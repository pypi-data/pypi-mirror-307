from cairo import FONT_SLANT_NORMAL, FONT_WEIGHT_BOLD, FONT_WEIGHT_NORMAL, Context, SVGSurface


class Cairo:
    def __init__(self, dungeon, filename, grid_size, offset=1):
        self._dungeon = dungeon
        self._filename = filename
        self._grid_size = grid_size
        self._offset = offset

        self._surface = SVGSurface(
            self._filename + ".svg",
            (dungeon.width + offset * 2) * grid_size,
            (dungeon.height + offset * 2) * grid_size,
        )
        self._context = Context(self._surface)

    def __del__(self):
        self._context.save()
        self._surface.write_to_png(self._filename + ".png")
        self._surface.finish()

    @property
    def dungeon(self):
        return self._dungeon

    def draw(self):
        ctx = self._context
        gs = self._grid_size

        # Draw a full black background
        self._context.set_source_rgb(0, 0, 0)
        self._context.paint()

        # Draw an internal white square inside
        ctx.set_source_rgb(1, 1, 1)
        self.rectangle(0, 0, self.dungeon.width, self.dungeon.height)
        ctx.fill()
        ctx.stroke()

        # Draw gray grid lines
        ctx.set_line_width(1.0)
        ctx.set_source_rgb(0.5, 0.5, 0.5)
        # skip first and last line
        for i in range(self.dungeon.width + 1):
            if i == 0 or i == self.dungeon.width:
                continue
            self.line(i, 0, 0, self.dungeon.height)
            ctx.stroke()
        for j in range(self.dungeon.height + 1):
            if j == 0 or j == self.dungeon.height:
                continue
            self.line(0, j, self.dungeon.width, 0)
            ctx.stroke()

        # Blacken every cell
        for i in range(self.dungeon.width):
            for j in range(self.dungeon.height):
                cell = self._dungeon.cells[i][j]
                if cell.is_occupied():
                    continue
                ctx.set_source_rgb(0, 0, 0)
                self.rectangle(i, j, 1, 1)
                ctx.fill()
                ctx.stroke()

        # print deadends
        ctx.set_source_rgb(1, 0, 0)
        ctx.set_font_size(12)
        ctx.select_font_face("Arial", FONT_SLANT_NORMAL, FONT_WEIGHT_NORMAL)
        for i in range(self._dungeon.width):
            for j in range(self._dungeon.height):
                cell = self.dungeon.cells[i][j]
                if not cell._deadend:
                    continue
                msg = "D"
                ctx.move_to((i + 0.1 + self._offset) * gs, (j + 0.6 + self._offset) * gs)
                ctx.show_text(msg)

        # # print cell identifiers
        # ctx.set_source_rgb(1, 0, 0)
        # ctx.set_font_size(12)
        # ctx.select_font_face("Arial", FONT_SLANT_NORMAL, FONT_WEIGHT_NORMAL)
        # for i in range(self._dungeon.width):
        #     for j in range(self._dungeon.height):
        #         cell = self.dungeon.cells[i][j]
        #         identifier = cell.identifier
        #         if identifier is None:
        #             continue
        #         msg = str(identifier)
        #         ctx.move_to((i + 0.1 + self._offset) * gs, (j + 0.6 + self._offset) * gs)
        #         ctx.show_text(msg)

        # # print cell id according to nwn tileset
        # ctx.set_source_rgb(1, 0, 0)
        # ctx.set_font_size(12)
        # ctx.select_font_face("Arial", FONT_SLANT_NORMAL, FONT_WEIGHT_NORMAL)
        # identifier = 0
        # for j in range(self._dungeon.height, 0, -1):
        #     j -= 1
        #     for i in range(self._dungeon.width):
        #         cell = self.dungeon.cells[i][j]
        #         ctx.move_to((i + 0.1 + self._offset) * gs, (j + 0.6 + self._offset) * gs)
        #         ctx.show_text(str(identifier))
        #         identifier += 1

        # Show room identifiers
        ctx.set_source_rgb(0, 0, 1)
        ctx.set_font_size(16)
        ctx.select_font_face("Arial", FONT_SLANT_NORMAL, FONT_WEIGHT_BOLD)
        for room in self.dungeon.walk_rooms():
            identifier = str(room.identifier)
            ctx.move_to((room.x + 1 + self._offset) * gs, (room.y + 1 + self._offset) * gs)
            ctx.show_text(identifier)
            ctx.stroke()

    def rectangle(self, x, y, width, height):
        ctx = self._context
        gs = self._grid_size

        x = x + self._offset
        y = y + self._offset
        width = width
        height = height
        ctx.rectangle(x * gs, y * gs, width * gs, height * gs)

    def move_to(self, x, y):
        ctx = self._context
        gs = self._grid_size
        ctx.move_to(gs * (x + self._offset), gs * (y + self._offset))

    def line_to(self, x, y):
        ctx = self._context
        gs = self._grid_size
        ctx.line_to(gs * (x + self._offset), gs * (y + self._offset))

    def line(self, x1, y1, width, height):
        self.move_to(x1, y1)
        self.line_to(x1 + width, y1 + height)
