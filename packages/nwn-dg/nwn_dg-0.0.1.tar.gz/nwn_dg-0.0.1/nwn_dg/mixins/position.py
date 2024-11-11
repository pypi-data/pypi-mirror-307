class PositionMixin:
    def __init__(self, x=None, y=None):
        self._x = x
        self._y = y

    def set_position(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y
