import heapq
from dataclasses import dataclass
from typing import Dict, Set, List, Generator, Callable
from itertools import groupby

from abacura_kallisti.atlas.wilderness import WildernessGrid
from abacura_kallisti.atlas.world import World
from abacura_kallisti.atlas.room import Exit, Room, Area
from abacura_kallisti.mud.player import PlayerCharacter
from itertools import chain

HOMETOWN = 'Midgaard City'
HOME_AREA_NAME = 'Mortal Residences'


@dataclass(slots=True)
class TravelStep:
    vnum: str
    exit: Exit
    cost: float


class TravelPath:
    def __init__(self, destination: Room = None):
        self.steps: List[TravelStep] = []
        self.destination: Room = destination

    def add_step(self, step: TravelStep):
        self.steps.append(step)

    def reverse(self):
        self.steps.reverse()

    def truncate_remaining_path(self, current_vnum: str) -> bool:
        """
        Determines if the current_vnum is on the path.
        If it is, it truncates the path to start from that vnum and returns True.
        If it is not on the path, it returns False
        """
        for i, step in enumerate(self.steps):
            if step.vnum == current_vnum:
                self.steps = self.steps[i:]
                return True

        return False

    def get_steps(self, vnum: str) -> Generator[TravelStep, None, None]:
        for step in self.steps:
            if step.vnum == vnum:
                yield step

    def get_travel_cost(self) -> float:
        return sum(s.cost for s in self.steps)

    def get_simplified_path(self):
        #     exits = room.known_exits
        #     exits = [e for e in exits.values() if is_allowed(e.to_vnum)]
        #     exits.sort(key=lambda x: area_tracking[x.to_vnum])
        # return speedwalk style directions
        if len(self.steps) == 0:
            return ''

        commands = [cmd for step in self.steps for cmd in step.exit.get_commands()]
        grouped = [(len(list(g)), cmd) for cmd, g in groupby(commands)]
        simplified = [f"{cnt if cnt > 1 else ''}{cmd}" for cnt, cmd in grouped]

        return ";".join(simplified)


@dataclass(slots=True)
class SpecialExit:
    check: Callable
    exit: Exit


class TravelGuide:

    def __init__(self, world: World, pc: PlayerCharacter, level: int = 0, avoid_home: bool = False):
        super().__init__()
        self.world: World = world
        self.wilderness_grid = WildernessGrid()
        # self.knows_bifrost = self.pc.probably_knows('Bifrost')
        self.exit_costs: dict = {}
        self.pc: PlayerCharacter = pc
        self.level = level
        self.avoid_home = avoid_home
        self.metrics = {}

    def get_path_to_room(self, start_vnum: str, goal_vnum: str,
                         avoid_vnums: Set[str], allowed_vnums: Set[str] = None) -> TravelPath:
        try:
            if start_vnum not in self.world.rooms:
                return TravelPath()

            path = next(self._gen_nearest_rooms(start_vnum, {goal_vnum}, avoid_vnums, allowed_vnums))
            return path
        except StopIteration:
            return TravelPath()

    def get_nearest_rooms_in_set(self, start_vnum: str, goal_vnums: Set[str],
                                 avoid_vnums: Set[str] = None, allowed_vnums: Set[str] = None,
                                 max_rooms: int = 1) -> List[TravelPath]:
        if avoid_vnums is None:
            avoid_vnums = set()

        # self.session.debug('NAV avoid %s' % avoid_vnums, show=True)
        found = []
        for path in self._gen_nearest_rooms(start_vnum, goal_vnums, avoid_vnums, allowed_vnums):
            found.append(path)
            if len(found) == max_rooms:
                break

        return found

    def _convert_came_from_to_path(self, dest_vnum: str, came_from: Dict) -> TravelPath:
        if dest_vnum not in self.world.rooms:
            return TravelPath()

        path = TravelPath(self.world.rooms[dest_vnum])

        current_vnum = dest_vnum

        while current_vnum in came_from and came_from[current_vnum][1].to_vnum != '':
            current_vnum, room_exit, cost = came_from[current_vnum]

            path.add_step(TravelStep(current_vnum, room_exit, cost))
            # add command to open door after the door because we will reverse below

        path.reverse()

        # translate from running cost to actual cost per step
        last_cost = 0
        for s in path.steps:
            s.cost, last_cost = s.cost - last_cost, s.cost

        return path

    def _get_special_exits(self) -> List[SpecialExit]:
        def can_go_home(room: Room):
            if room.area_name == "The Wilderness":
                return False
            home_allowed = room.area_name in [HOMETOWN, HOME_AREA_NAME]
            has_home = self.pc.home_vnum != ''
            return not self.avoid_home and home_allowed and has_home

        def can_depart(room: Room):
            if room.area_name == "The Wilderness":
                return False

            is_home = room.area_name == HOME_AREA_NAME
            has_egress = self.pc.egress_vnum != ''
            return not self.avoid_home and is_home and has_egress

        def can_recall(room: Room):
            if room.area_name == "The Wilderness":
                return False

            recall_allowed = not room.no_recall and not room.silent and not room.no_magic
            has_recall = self.pc.recall_vnum != ''
            return recall_allowed and has_recall

        return [
            SpecialExit(can_go_home, Exit(to_vnum=self.pc.home_vnum, direction='home', weight=2)),
            SpecialExit(can_depart, Exit(to_vnum=self.pc.egress_vnum, direction='depart', weight=2)),
            SpecialExit(can_recall, Exit(to_vnum=self.pc.recall_vnum, direction='recall', weight=3)),
        ]

    def _get_wilderness_cost(self, current_room: Room, room_exit: Exit, goal_vnums: set) -> int:
        cost = 0

        if len(goal_vnums) != 1:
            return cost

        # increase cost if we are going further away from our single goal room
        goal_vnum = list(goal_vnums)[0]
        cur_distance = self.wilderness_grid.get_distance(current_room.vnum, goal_vnum)
        new_distance = self.wilderness_grid.get_distance(room_exit.to_vnum, goal_vnum)
        cost += 5 * (new_distance - cur_distance)

        return cost

    def _gen_nearest_rooms(self, start_vnum: str, goal_vnums: Set[str], avoid_vnums: Set[str],
                           allowed_vnums: Set[str] = None) -> Generator[TravelPath, None, None]:

        # This is a priority queue using heapq, the lowest weight item will heappop() off the list
        frontier = []
        goal_vnums = goal_vnums.copy()
        heapq.heappush(frontier, (0, start_vnum))

        came_from: Dict[str, (str, Exit, int)] = {start_vnum: (start_vnum, Exit(), 0)}
        cost_so_far = {start_vnum: 0}

        special_exits = self._get_special_exits()

        # explore_areas = set(self.world.rooms[vnum].area_name for vnum in goal_vnums)
        # explore_areas.add(self.world.rooms[start_vnum].area_name)
        # skip_areas = set()
        # self.metrics['skip_areas'] = len(skip_areas)

        n = 0
        while len(frontier) > 0 and n <= 60000:
            n += 1
            current_cost, current_vnum = heapq.heappop(frontier)

            if current_vnum in goal_vnums:
                # self.session.debug('NAV: gen examined %d rooms' % len(came_from))
                # self.metrics['areas skipped'] = len(skip_areas)
                self.metrics['rooms visited'] = n
                yield self._convert_came_from_to_path(current_vnum, came_from)

            current_room = self.world.rooms[current_vnum]

            # Future optimization, don't look in areas that don't lead to unvisited rooms
            # current_area = current_room.area_name
            # if current_area not in explore_areas and current_area not in skip_areas:
            #     if current_area in self.world.area_transits:
            #         transits = self.world.area_transits[current_area]
            #         if all([vnum in came_from for vnum in transits]):
            #             skip_areas.add(current_area)
            #             # self.metrics['skip_areas'] = skip_areas
            #             continue
            #     explore_areas.add(current_area)

            if current_room.vnum in avoid_vnums:
                continue

            if allowed_vnums and current_vnum not in allowed_vnums:
                continue

            if current_room.deathtrap or current_room.terrain.impassable:
                continue

            room_se = [se.exit for se in special_exits if se.exit.to_vnum not in came_from and se.check(current_room)]

            for room_exit in chain(current_room.exits.values(), room_se):

                if room_exit.to_vnum in came_from and room_exit.to_vnum not in goal_vnums:
                    continue

                if room_exit.locks:
                    continue

                if not (room_exit.max_level >= self.level >= room_exit.min_level):
                    continue

                to_room = self.world.rooms.get(room_exit.to_vnum, None)
                if to_room is None:
                    continue

                # compute cost
                new_cost = cost_so_far.get(current_vnum, 0) + to_room.terrain.weight
                if current_room.area_name == 'The Wilderness':
                    new_cost += self._get_wilderness_cost(current_room, room_exit, goal_vnums)

                if room_exit.to_vnum not in cost_so_far or new_cost < cost_so_far[room_exit.to_vnum]:
                    heapq.heappush(frontier, (new_cost, room_exit.to_vnum))
                    # print('Put: ', current_vnum, room_exit.direction, room_exit.to_vnum, new_cost)
                    cost_so_far[room_exit.to_vnum] = new_cost
                    came_from[room_exit.to_vnum] = (current_vnum, room_exit, new_cost)

    def is_navigable_room_in_area(self, area: Area, vnum: str) -> bool:
        vnum_allowed = area.is_allowed_vnum(vnum, self.level)
        vnum_mapped = vnum in self.world.rooms
        if not vnum_allowed or not vnum_mapped:
            return False

        room = self.world.rooms[vnum]
        area_allowed = area.is_allowed_area(room.area_name)
        return vnum_mapped and vnum_allowed and area_allowed

    # def get_avoid_rooms_in_known_area(self, start_vnum: str) -> set:
    #     room: Room = self.world.rooms[start_vnum]
    #     ea = KNOWN_AREAS[room.area_name]
    #     return known_area.get_excluded_room_vnums(self.char_level)
    #
    def get_reachable_rooms_in_known_area(self, start_vnum: str, area: Area,
                                          allowed_rooms: Set[str] = None, max_steps: int = 999999,
                                          consider_locks_reachable: bool = False) -> set:
        visited = set()
        frontier = {start_vnum}
        room: Room = self.world.rooms[start_vnum]

        if area.track_random_portals:
            vnums = [r.vnum for r in self.world.rooms.values() if r.area_name == room.area_name]
            vnums = [v for v in vnums if self.is_navigable_room_in_area(area, v)]
            vnums = [v for v in vnums if allowed_rooms is None or v in allowed_rooms]
            return set(vnums)

        while len(frontier) > 0 and max_steps > 0:
            max_steps -= 1
            room_vnum = frontier.pop()
            if room_vnum not in self.world.rooms:
                continue

            visited.add(room_vnum)
            # room = self.world.rooms[room_vnum]

            for e in self.world.rooms[room_vnum].exits.values():
                if not self.is_navigable_room_in_area(area, e.to_vnum):
                    continue

                if allowed_rooms is not None and e.to_vnum not in allowed_rooms:
                    continue

                unreachable_lock = e.locks and not consider_locks_reachable
                if e.to_vnum not in visited and e.to_vnum not in frontier and not unreachable_lock:
                    frontier.add(e.to_vnum)

        return visited
