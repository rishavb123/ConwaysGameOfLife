import pickle
from enum import Enum
import pygame

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
    
    def rotate_right(self):
        self.alive_cells = set((-cell[1], cell[0]) for cell in self.alive_cells)
        return self
    
    def rotate_left(self):
        return self.rotate_right().rotate_right().rotate_right()

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
            alive_cells = Configuration(pickle.load(f))
            self.place(alive_cells, loc=loc)
        return self