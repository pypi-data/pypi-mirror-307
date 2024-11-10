"""LOK MSDP plugin"""
from __future__ import annotations

from dataclasses import asdict, fields

from rich.panel import Panel
from rich.pretty import Pretty

from abacura_kallisti.mud.affect import Affect
from abacura_kallisti.plugins import LOKPlugin

from abacura.mud.options.msdp import MSDPMessage
from abacura.plugins import command
from abacura.plugins.events import event


# TODO: disable the abacura @msdp command and let's implement it here
class LOKMSDP(LOKPlugin):

    def __init__(self):
        super().__init__()
        self.msdp_types = {f.name: f.type for f in fields(self.msdp)}
        print(self.msdp_types)

    @command(name="lokmsdp")
    def lok_msdp_command(self, variable: str = '', reportable: bool = False) -> None:
        """Dump MSDP values for debugging"""
        if not self.msdp.reportable_variables:
            self.session.output("[bold red]# MSDPERROR: MSDP NOT LOADED?", markup=True)

        if not variable:
            d = asdict(self.msdp)
            if not reportable:
                d.pop("reportable_variables")
            panel = Panel(Pretty(d), highlight=True)
        else:
            value = getattr(self.msdp, variable)
            panel = Panel(Pretty(value), highlight=True)

        self.session.output(panel, highlight=True, actionable=False)

    @event("msdp_value", priority=1)
    def update_lok_msdp(self, message: MSDPMessage):
        # self.msdp.values[message.type] = message.value
        attr_name = message.type.lower()

        renames = {'class': 'cls', 'str': 'str_', 'int': 'int_'}
        attr_name = renames.get(attr_name, attr_name)

        if attr_name == 'ranged':
            pass

        # if not hasattr(self.msdp, attr_name):
        #     self.output(f"[red]Missing msdp attribute {attr_name} {message.type}", markup=True)
        #     return

        value = message.value
        if self.msdp_types[attr_name] == int:
            value = 0 if len(message.value) == 0 else int(message.value)
        elif self.msdp_types[attr_name] == str:
            value = str(message.value)

        if attr_name == 'group':
            self.msdp.group.update_members_from_msdp(value)
            self.msdp.group.update_members_from_msdp(value)
        elif attr_name == 'affects' and type(value) is dict:
            self.msdp.affects = sorted([Affect(name, hrs) for name, hrs in value.items()], key=lambda a: a.name)
        else:
            setattr(self.msdp, attr_name, value)

        # if name == 'MSDP_CHARACTER_NAME':
        #     self.dispatcher.dispatch(event.Event(event.NEW_CHARACTER, value))
