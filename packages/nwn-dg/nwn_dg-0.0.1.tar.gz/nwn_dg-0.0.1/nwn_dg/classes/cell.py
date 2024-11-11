from enum import Enum

from ..mixins import IdentifierMixin, PositionMixin


class FloorType(Enum):
    NONE = 0
    ROOM_FLOOR = 1
    CORRIDOR = 2


class Cell(IdentifierMixin, PositionMixin):
    def __init__(self, floor_type=FloorType.NONE):
        IdentifierMixin.__init__(self)
        PositionMixin.__init__(self)

        self._floor_type = floor_type

        # Cell is a part of a room exit
        self._sill = None

        # Cell favored direction
        self._direction = None

        self._deadend = False
        self._room_identifier = None

    def __repr__(self):
        retval = {
            "x": self.x,
            "y": self.y,
            "identifier": self.identifier,
            "direction": self.direction,
        }
        return str(retval)

    def set_floor(self):
        self._identifier = None
        self._room_identifier = None
        self._floor_type = FloorType.NONE

    def set_room(self, identifier):
        self._identifier = identifier
        self._room_identifier = identifier
        self._floor_type = FloorType.ROOM_FLOOR

    def set_sill(self, identifier, direction):
        self._identifier = identifier
        self._room_identifier = None
        self._sill = True
        self._direction = direction

    def disable_sill(self, clear_id=False):
        if clear_id:
            self._identifier = None
            self._room_identifier = None
        self._sill = None

    def set_corridor(self, identifier, direction):
        self._identifier = identifier
        self._room_identifier = None
        self._floor_type = FloorType.CORRIDOR
        self._direction = direction

    def is_possible_sill(self):
        return not (self._sill or self._floor_type in [FloorType.ROOM_FLOOR, FloorType.CORRIDOR])

    def is_corridor_sill(self):
        return self._sill and self._floor_type in [FloorType.CORRIDOR]

    def is_occupied(self):
        return self._floor_type in [FloorType.ROOM_FLOOR, FloorType.CORRIDOR]

    def is_corridor(self):
        return self._floor_type == FloorType.CORRIDOR

    def is_room(self):
        return self._floor_type == FloorType.ROOM_FLOOR

    @property
    def direction(self):
        return self._direction
