import random
from enum import Enum


class Position(Enum):
    Leaf = 0
    Left = 1
    Right = 2
    Top = 3
    Bottom = 4


class SplitType(Enum):
    Leaf = 0
    Horizontal = 1
    Vertical = 2


class Node:
    def __init__(self, x, y, width, height):
        # We count in cells, we're 1 based.
        self._x = x
        self._y = y
        self._width = width
        self._height = height

        self._split_type = SplitType.Leaf
        self._position = Position.Leaf

        self._associate = None
        self._children = []

    #        self.room = None

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def split_type(self):
        return self._split_type

    @split_type.setter
    def split_type(self, rhs):
        self._split_type = rhs

    @property
    def associate(self):
        return self._associate

    @associate.setter
    def associate(self, rhs):
        self._associate = rhs

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, rhs):
        self._children = rhs

    def walk(self):
        yield self
        for item in self._children:
            yield from item.children

    # TODO: handle a max_ratio for left and right
    def _split_r(self, min_split_length, current_depth=0):
        # Can we split in said position?
        x_min = self.x + min_split_length
        x_max = self.x - min_split_length + self.width
        y_min = self.y + min_split_length
        y_max = self.y - min_split_length + self.height

        is_horizontal = x_min <= x_max
        is_vertical = y_min <= y_max
        if not is_horizontal and not is_vertical:
            return False

        # If we can split in both positions, just choose one
        if is_horizontal and is_vertical:
            is_horizontal = bool(random.randint(0, 1))
            is_vertical = not is_horizontal

        if is_horizontal:
            self._split_type = SplitType.Horizontal
            split_x = random.randint(x_min, x_max)

            child_1 = Node(self.x, self.y, split_x - self.x, self.height)
            child_2 = Node(split_x, self.y, self.x + self.width - split_x, self.height)
            child_1.position = Position.Left
            child_2.position = Position.Right

        if is_vertical:
            self._split_type = SplitType.Vertical
            split_y = random.randint(y_min, y_max)

            child_1 = Node(self.x, self.y, self.width, split_y - self.y)
            child_2 = Node(self.x, split_y, self.width, self.y + self.height - split_y)
            child_1.position = Position.Top
            child_2.position = Position.Bottom

        child_1.associate = child_2
        child_2.associate = child_1

        child_1._split_r(min_split_length, current_depth + 1)
        child_2._split_r(min_split_length, current_depth + 1)
        self.children += [child_1, child_2]
        return True

    def split(self, min_split_length):
        return self._split_r(min_split_length)


#    def create_room(self, room_generator_fn, margin):
#        max_width = self.width - margin * 2
#        max_height = self.height - margin * 2
#        width, height = room_generator_fn(max_width, max_height)
#        width = min(width, max_width)
#        height = min(height, max_height)
#
#        x = random.randint(self.x + margin, self.x + self.width - width - 1)
#        y = random.randint(self.y + margin, self.y + self.height - height - 1)
#        self.room = Room(x, y, width, height)
#        self.room.node = weakref.ref(self)
#        return self.room


class BSPGenerator(Node):
    def __init__(self, dungeon, min_split_length):
        Node.__init__(self, 1, 1, dungeon.width, dungeon.height)

        self.split(min_split_length)
        self.create_rooms(dungeon.room_generator_fn, dungeon.room_spacer)

    def create_rooms(self, room_generator_fn, room_spacer=1):
        for node in self.walk():
            if not node.split_type == SplitType.Leaf:
                continue
            node.create_room(room_generator_fn, room_spacer)


#            self._rooms += [room]
