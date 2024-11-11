from ..mixins import DimensionsMixin, IdentifierMixin, PositionMixin


class Room(IdentifierMixin, DimensionsMixin, PositionMixin):
    def __init__(self, width, height):
        IdentifierMixin.__init__(self)
        DimensionsMixin.__init__(self, width, height)
        PositionMixin.__init__(self)

        self._current_identifier = self._identifier

    @property
    def current_identifier(self):
        if self._current_identifier is None:
            self._current_identifier = self._identifier
        return self._current_identifier

    @current_identifier.setter
    def current_identifier(self, rhs):
        self._current_identifier = rhs
