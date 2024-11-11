import copy
import math
import random

from ..classes import DIRECTIONS, Directions, get_new_coordinates


class Scattered:
    def __init__(self, dungeon, room_generator_fn):
        # TODO: verify that dungeon width and height are odd numbers
        self._dungeon = dungeon
        self._cells = dungeon.cells
        self._width = dungeon.width
        self._height = dungeon.height

        self._room_generator_fn = room_generator_fn
        self._open_cells = []
        self._deadends = []

        self.create_rooms()
        self.open_rooms()
        while len(self._open_cells):
            self.tunnel()
        self.remove_unaccessible()
        self._deadends = self.remove_deadends()

        # TODO: Reschape rooms if possible, cutting corners, ...
        # TODO: Place doors, etc.

    def create_rooms(self):
        # TODO: divide area by room area
        room_count = 20
        for i in range(room_count):
            # TODO: verify that room width and height are odd numbers
            room = self._room_generator_fn()
            self.emplace_room(room)

    def emplace_room(self, room):
        tentatives = 10
        while tentatives > 0:
            # Find a random place, and try to place it
            x = (random.randint(0, self._width - room.width) // 2) * 2
            y = (random.randint(0, self._height - room.height) // 2) * 2
            room.set_position(x, y)

            tentatives -= 1
            if self._dungeon.add_room(room):
                return

    def open_rooms(self):
        def get_opening_count(room):
            room_h = int((room.height / 2) + 1)
            room_w = int((room.width / 2) + 1)
            openings = int(math.sqrt(room_h * room_w))
            openings + random.randint(0, max(openings - 1, 0))
            openings = max(openings, 1)
            return openings

        # Build a list of all rooms and sills, marking cells as sills
        for room in self._dungeon.walk_rooms():
            # temporary variable for the length of this function
            room.sills = self.get_sills(room)
            random.shuffle(room.sills)

        # Second pass to open sills
        for room in self._dungeon.walk_rooms():
            n_opens = get_opening_count(room)
            n_opens = min(n_opens, len(room.sills))

            for i in range(n_opens):
                sill = room.sills.pop(0)

                x2, y2 = get_new_coordinates(sill.x, sill.y, sill.direction)
                cell1 = self._dungeon.cells[sill.x][sill.y]
                cell2 = self._dungeon.cells[x2][y2]

                # cell1 and cell2 reach out into the open
                if not cell2.is_occupied():
                    cell1.set_corridor(room.current_identifier, sill.direction)
                    cell1.disable_sill()

                    cell2.set_corridor(room.current_identifier, sill.direction)
                    self._open_cells += [cell2]
                    continue

                # cell1 (a sill) connects to a room or a corridor
                if cell2.is_room() or cell2.is_corridor():
                    cell1.set_corridor(room.current_identifier, sill.direction)
                    cell1.disable_sill()
                    self._dungeon.merge_identifiers([cell1.identifier, cell2.identifier])

                    # cell1 (a sill) connects to cell2 (a corridor)
                    if cell2.is_corridor():
                        cell2.set_corridor(room.current_identifier, sill.direction)
                        self._open_cells += [cell2]
                        continue

        # Nuke remaining sills
        for room in self._dungeon.walk_rooms():
            for sill in room.sills:
                cell = self._dungeon.cells[sill.x][sill.y]
                cell.disable_sill(True)
            del room.sills

    def get_sills(self, room):
        sills = []
        if room.x >= 2:  # West border
            for y in range(0, room.height, 2):
                sills += [self.check_sill(room, 0, y, Directions.WEST)]
        if room.y >= 2:  # North border
            for x in range(0, room.width, 2):
                sills += [self.check_sill(room, x, 0, Directions.NORTH)]
        if room.x <= (self._dungeon.width - room.width - 1):  # East border
            for y in range(0, room.height, 2):
                sills += [self.check_sill(room, room.width - 1, y, Directions.EAST)]
        if room.y <= (self._dungeon.height - room.height - 1):  # South border
            for x in range(0, room.width, 2):
                sills += [self.check_sill(room, x, room.height - 1, Directions.SOUTH)]
        sills = [sill for sill in sills if sill is not None]
        return sills

    def check_sill(self, room, x, y, direction):
        x, y = get_new_coordinates(room.x + x, room.y + y, direction)
        cell = self._cells[x][y]
        if cell.is_possible_sill():
            cell.set_sill(room.identifier, direction)
            return cell
        return None

    def tunnel(self):
        def get_tunnel_direction(last_dir):
            # TODO: make this a parameter
            bend_chance = 50

            retval = copy.deepcopy(DIRECTIONS)
            random.shuffle(retval)
            if last_dir and random.randint(0, 100) < bend_chance:
                retval.insert(0, last_dir)
            return retval

        if not len(self._open_cells):
            return

        random.shuffle(self._open_cells)
        n_cell = self._open_cells.pop(0)
        self._open_cells = [cell for cell in self._open_cells if not (cell.x == n_cell.x and cell.y == n_cell.y)]

        x1 = n_cell.x
        y1 = n_cell.y
        directions = get_tunnel_direction(n_cell.direction)
        for direction in directions:
            x2, y2 = get_new_coordinates(x1, y1, direction)
            x3, y3 = get_new_coordinates(x2, y2, direction)

            if x2 < 0 or x3 < 0 or y2 < 0 or y2 < 0:
                continue
            if x2 >= self._width or x3 >= self._width or y2 >= self._height or y2 >= self._height:
                continue

            cell2 = self._cells[x2][y2]
            cell3 = self._cells[x3][y3]

            if not cell2.is_occupied():
                if cell3.is_room():
                    n_cell.set_corridor(n_cell.identifier, direction)
                    continue
                # If we land on an empty space, then it's OK
                if not cell3.is_occupied():
                    n_cell.set_corridor(n_cell.identifier, direction)
                    cell2.set_corridor(n_cell.identifier, direction)
                    cell3.set_corridor(n_cell.identifier, direction)
                    self._open_cells += [n_cell]
                    self._open_cells += [cell3]
                    return
                if cell3.is_corridor():
                    if n_cell.identifier != cell3.identifier:
                        id1 = n_cell.identifier
                        id2 = cell3.identifier
                        n_cell.set_corridor(n_cell.identifier, direction)
                        cell2.set_corridor(n_cell.identifier, direction)
                        cell3.set_corridor(n_cell.identifier, direction)
                        self._open_cells += [n_cell]
                        self._open_cells += [cell3]
                        self._dungeon.merge_identifiers([id1, id2])
        else:
            n_cell.set_corridor(n_cell.identifier, None)
            self._deadends += [n_cell]

    def remove_unaccessible(self):
        # NOTE: This doesn't remove the rooms, nor from deadends
        for x in range(self._width):
            for y in range(self._height):
                cell = self._cells[x][y]
                if cell.identifier not in [None, 1]:
                    cell.set_floor()

    def remove_deadends(self):
        def get_exits(cell):
            exits = []
            for direction in DIRECTIONS:
                x, y = get_new_coordinates(cell.x, cell.y, direction)
                if x < 0 or y < 0:
                    continue
                if x >= self._width or y >= self._height:
                    continue
                if self._cells[x][y].is_occupied():
                    exits += [self._cells[x][y]]
            return exits

        # Reduce possible deadends to real deadends
        deadends = []
        for cell in self._deadends:
            if len(get_exits(cell)) <= 1:
                deadends += [cell]

        if len(deadends) == 0:
            return

        # TODO: parameter 50%
        deadend_pct = 0.30
        k = int(len(deadends) * (1.0 - min(max(float(deadend_pct), 0.0), 1.0)))
        k = min(max(0, k), len(deadends))
        # deadends to remove
        rm_deadends = random.sample(deadends, k)
        # return deadends that aren't removed
        retval = [item for item in deadends if item not in rm_deadends]
        for cell in retval:
            self._cells[cell.x][cell.y]._deadend = True

        # Delete deadends
        while len(rm_deadends):
            cell = rm_deadends.pop(0)
            exits = get_exits(cell)
            if len(exits) <= 1:
                self._cells[cell.x][cell.y].set_floor()
                rm_deadends += exits
        return retval
