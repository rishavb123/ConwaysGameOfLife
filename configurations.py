import pickle
from enum import Enum

class RenderType(Enum):
    PRINT_STATE=0
    PYGAME=1

class Configuration:

    def __init__(self, alive_cells=None, render_type=RenderType.PRINT_STATE):
        self.alive_cells = set(alive_cells if alive_cells is not None else ())
        self.set_render_type(render_type)

    def set_cell(self, pos):
        self.alive_cells.add(pos)
        return self

    def clear_cell(self, pos):
        if pos in self.alive_cells:
            self.alive_cells.remove(pos)
            return self

    def set_cells(self, pos_arr):
        [self.set_cell(pos) for pos in pos_arr]
        return self

    def clear_cells(self, pos_arr):
        [self.clear_cell(pos) for pos in pos_arr]
        return self
    
    def clear(self):
        self.alive_cells.clear()
        return self

    def flip_cell(self, pos):
        if pos in self.alive_cells:
            self.alive_cells.remove(pos)
        else:
            self.alive_cells.add(pos)
            return self

    def flip_cells(self, pos_arr):
        [self.flip_cell(pos) for pos in pos_arr]
        return self

    def is_set(self, pos):
        return pos in self.alive_cells

    def set_render_type(self, render_type):
        self.render_type = render_type
        return self

    def place(self, config, loc=(0, 0)):
        if callable(config):
            config = config()
        self.set_cells([(cell[0] + loc[0], cell[1] + loc[1]) for cell in config.alive_cells])
        return self

    def shift(self, loc=(0, 0)):
        c = self.__class__()
        c.set_cells([(cell[0] + loc[0], cell[1] + loc[1]) for cell in self.alive_cells])
        self.alive_cells = c.alive_cells
        return self
    
    def shift_to_origin(self):
        min_x = min(self.alive_cells, key=lambda x: x[0])[0]
        min_y = min(self.alive_cells, key=lambda y: y[1])[1]
        self.shift(loc=(-min_x, -min_y))
        return self
    
    def rotate_cw(self):
        self.alive_cells = set((-cell[1], cell[0]) for cell in self.alive_cells)
        return self
    
    def rotate_ccw(self):
        return self.rotate_cw().rotate_cw().rotate_cw()

    def copy(self):
        c = self.__class__()
        c.alive_cells = self.alive_cells.copy()
        return c

    def render(self, **kwargs):
        if self.render_type == RenderType.PRINT_STATE:
            print("State:", self.alive_cells)
        elif self.render_type == RenderType.PYGAME:
            screen = kwargs["screen"]
            color = kwargs.get("color", "#000")
            bg_color = kwargs.get("bg_color", None)
            ox, oy = kwargs.get("origin", (0, 0))
            pygame = kwargs["pygame"]

            w = screen.get_width()
            h = screen.get_height()

            cell_size = kwargs.get("cell_size", w / 10)

            if bg_color is not None:
                screen.fill(bg_color)

            for cell in self.alive_cells:
                i, j = cell
                sx = ox + i * cell_size
                sy = oy + j * cell_size

                if -cell_size < sx < w and -cell_size < sy < h:
                    pygame.draw.rect(surface=screen, color=color, rect=(sx, sy, cell_size, cell_size))


    def save(self, fname):
        with open(fname, "wb") as f:
            shifted = self.copy().shift_to_origin()
            pickle.dump(shifted.alive_cells, f)
        return self

    def load(self, fname, loc=(0, 0)):
        with open(fname, "rb") as f:
            c = Configuration(pickle.load(f))
            self.place(c, loc=loc)
        return self
    
    def load_from_lexicon(self, lexicon_name, loc=(0, 0)):
        with open("./lexicon/lexicon.txt") as f:
            found = False
            y = -1
            c = Configuration()
            for line in f:
                if not found:
                    if line.lower().startswith(f":{lexicon_name.lower()}:"):
                        found = True
                else:
                    if y < 0:
                        if line.startswith(":"):
                            break
                        if line.startswith("\t"):
                            y = 0
                    if y >= 0:
                        if not line.startswith("\t"):
                            break
                        for x in range(len(line)):
                            if line[x] == '*':
                                c.set_cell((x, y))
                        y += 1
            if not found:
                raise ValueError(f"The pattern {lexicon_name} was not found in the lexicon.txt file. Make sure to specify the name of something in the lexicon.")
            if y < 0:
                raise ValueError(f"The pattern {lexicon_name} has no pattern in the lexicon.txt file. Make sure to specify the name of something that includes a pattern image in the lexicon.")
            self.place(c, loc=loc)