import pickle
from enum import Enum
import pygame

class RenderType(Enum):
    PRINT_STATE=0
    PYGAME=1

class Configuration:

    def __init__(self, render_type=RenderType.PRINT_STATE):
        self.alive_cells = set()
        self.set_render_type(render_type)

    def set_cell(self, pos):
        self.alive_cells.add(pos)

    def clear_cell(self, pos):
        if pos in self.alive_cells:
            self.alive_cells.remove(pos)

    def set_cells(self, pos_arr):
        [self.set_cell(pos) for pos in pos_arr]

    def clear_cells(self, pos_arr):
        [self.clear_cell(pos) for pos in pos_arr]

    def flip_cell(self, pos):
        if pos in self.alive_cells:
            self.alive_cells.remove(pos)
        else:
            self.alive_cells.add(pos)

    def flip_cells(self, pos_arr):
        [self.flip_cell(pos) for pos in pos_arr]

    def is_set(self, pos):
        return pos in self.alive_cells

    def set_render_type(self, render_type):
        self.render_type = render_type

    def place(self, config, loc=(0, 0)):
        if callable(config):
            config = config()
        self.set_cells([(cell[0] + loc[0], cell[1] + loc[1]) for cell in config.alive_cells])

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
            pickle.dump(self.alive_cells, f)
        return self

    def load(self, fname):
        with open(fname, "rb") as f:
            self.alive_cells = pickle.load(f)
        return self