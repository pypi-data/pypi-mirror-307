import matplotlib.pyplot as plt
import networkx as nx

from ..mixins import DimensionsMixin
from .cell import Cell


class Dungeon(DimensionsMixin):
    def __init__(self, width, height):
        DimensionsMixin.__init__(self, width, height)

        self._tree = []
        self._rooms = []
        self._cells = [[Cell() for x in range(width)] for y in range(height)]
        for x in range(self.width):
            for y in range(self.height):
                self._cells[x][y].set_position(x, y)

    def tree(self):
        G = nx.from_edgelist(self._tree)
        nx.draw(G, with_labels=True, font_weight="bold")
        plt.savefig("path.png")

    @property
    def cells(self):
        return self._cells

    def add_room(self, room):
        # Verify placement
        for x in range(room.width):
            for y in range(room.height):
                cell = self.cells[x + room.x][y + room.y]
                if cell.is_occupied():
                    return False

        # Add the room with an identifier (base 1)
        self._rooms += [room]
        room.identifier = len(self._rooms)

        # For every cell contained by this room, set the identifier
        for x in range(room.width):
            for y in range(room.height):
                cell = self.cells[x + room.x][y + room.y]
                cell.set_room(room.identifier)
        return True

    def merge_identifiers(self, identifiers):
        min_id = min(identifiers)

        self._tree += [identifiers]

        for room in self.walk_rooms():
            if room.current_identifier in identifiers:
                room.current_identifier = min_id

        for x in range(self.width):
            for y in range(self.height):
                cell = self._cells[x][y]
                if cell.identifier in identifiers:
                    cell.identifier = min_id

    def walk_rooms(self):
        yield from self._rooms

    def print_r(self):
        for j in range(self.height):
            for i in range(self.width):
                cell = self.cells[i][j]
                if cell.floor:
                    print("X", end="")
                else:
                    print(".", end="")
            print("")
