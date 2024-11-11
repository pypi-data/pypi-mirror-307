class Packed:
    def __init__(self, dungeon, room_generator_fn):
        self._dungeon = dungeon
        self._room_generator_fn = room_generator_fn

        self.create_rooms()

    def create_rooms(self):
        h_width = self._dungeon._width // 2
        h_height = self._dungeon._height // 2

        for i in range(h_width):
            for j in range(h_height):
                x = i * 2 + 1
                y = j * 2 + 1

                self._room_generator_fn(x, y)
