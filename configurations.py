import pickle
from enum import Enum
import numpy as np
import re

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

    def get_bounds(self):
        min_x = min(self.alive_cells, key=lambda x: x[0])[0]
        min_y = min(self.alive_cells, key=lambda y: y[1])[1]
        max_x = max(self.alive_cells, key=lambda x: x[0])[0]
        max_y = max(self.alive_cells, key=lambda y: y[1])[1]
        return min_x, max_x, min_y, max_y

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
        min_x, _, min_y, _ = self.get_bounds()
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
    
    def set_rules(self, born='3', stay='23'):
        return self

    def get_bounds(self):
        return (0, 0)

    def set_bounds(self, min_x=0, max_x=0, min_y=0, max_y=0):
        return self

    def render(self, **kwargs):
        if self.render_type == RenderType.PRINT_STATE:
            print("State:", self.alive_cells)
        elif self.render_type == RenderType.PYGAME:
            screen = kwargs["screen"]
            color = kwargs.get("color", "#000")
            bg_color = kwargs.get("bg_color", None)
            grid_color = kwargs.get("grid_color", None)
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

            if grid_color is not None:
                start_i = int(np.floor(-ox / cell_size))
                start_j = int(np.floor(-oy / cell_size))

                end_i = int(np.floor((w - ox) / cell_size))
                end_j = int(np.floor((h - oy) / cell_size))

                for i in range(start_i, end_i + 1):
                    sx = ox + i * cell_size
                    pygame.draw.line(surface=screen, color=grid_color, start_pos=(sx, 0), end_pos=(sx, h))

                for j in range(start_j, end_j + 1):
                    sy = oy + j * cell_size
                    pygame.draw.line(surface=screen, color=grid_color, start_pos=(0, sy), end_pos=(w, sy))

    def save(self, fname):
        if fname.split(".")[-1] != 'pkl':
            raise ValueError("File name must have the pkl extension.")
        with open(fname, "wb") as f:
            shifted = self.copy().shift_to_origin()
            pickle.dump(shifted.alive_cells, f)
        return self
    
    def load(self, name, loc=(0, 0)):
        if "." not in name:
            return self.load_from_lexicon(lexicon_name=name, loc=loc)
        ext = name.split(".")[-1]
        if ext == 'txt':
            return self.load_from_txt(fname=name, loc=loc)
        elif ext == 'pkl':
            return self.load_from_pkl(fname=name, loc=loc)
        elif ext == 'rle':
            return self.load_from_rle(fname=name, loc=loc)
        else:
            return self.load_from_lexicon(lexicon_name=name, loc=loc)

    def load_from_pkl(self, fname, loc=(0, 0)):
        with open(fname, "rb") as f:
            c = Configuration(pickle.load(f))
            self.place(c, loc=loc)
        return self
    
    def load_from_lexicon(self, lexicon_name, loc=(0, 0), lexicon_path="./configs/lexicon/lexicon.txt"):
        with open(lexicon_path) as f:
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
        return self

    def load_from_txt(self, fname, loc=(0, 0)):
        with open(fname) as f:
            y = 0
            c = Configuration()
            for line in f:
                if line.startswith("#"):
                    continue
                for x in range(len(line)):
                    if line[x] == '*':
                        c.set_cell((x, y))
                y += 1
            self.place(c, loc=loc)
        return self
    
    def load_from_rle(self, fname, loc=(0, 0)):
        with open(fname) as f:
            lines = f.readlines()
        lines = [line.strip() for line in lines]
        lines = [line for line in lines if len(line) == 0 or line[0] != '#']
        header = lines[0].lower()
        lines = lines[1:]
        lines = ''.join(lines).strip('\n')

        header_patterns = [
            re.compile(r'x\s?=\s?(\d+).*?y\s?=\s?(\d+).*?s(\d+).*?b(\d+).*?'),
            re.compile(r'x\s?=\s?(\d+).*?y\s?=\s?(\d+).*?b(\d+).*?s(\d+).*?'),
            re.compile(r'x\s?=\s?(\d+).*?y\s?=\s?(\d+).*?'),
            re.compile(r'y\s?=\s?(\d+).*?x\s?=\s?(\d+).*?s(\d+).*?b(\d+).*?'),
            re.compile(r'y\s?=\s?(\d+).*?x\s?=\s?(\d+).*?b(\d+).*?s(\d+).*?'),
            re.compile(r'y\s?=\s?(\d+).*?x\s?=\s?(\d+).*?'),
            re.compile(r'.*?'),
        ]

        var_reader = [
            dict(x=1, y=2, s=3, b=4),
            dict(x=1, y=2, b=3, s=4),
            dict(x=1, y=2, b='3', s='23'),
            dict(y=1, x=2, s=3, b=4),
            dict(y=1, x=2, b=3, s=4),
            dict(y=1, x=2, b='3', s='23'),
            dict(x='0', y='0', b='3', s='23')
        ]

        matches = None
        pattern_idx = 0

        while matches is None:
            if pattern_idx >= len(header_patterns):
                raise ValueError(f"The file {fname} does not have a header of any of the allowed formats. Please specify a valid file.")

            matches = header_patterns[pattern_idx].match(header)
            pattern_idx += 1

        pattern_idx -= 1

        def get_from_header(k):
            r = var_reader[pattern_idx][k]
            if type(r) == int:
                return matches.group(r)
            return r
        
        w = int(get_from_header('x'))
        h = int(get_from_header('y'))
        born = get_from_header('b')
        stay = get_from_header('s')

        self.set_rules(born=born, stay=stay)
    
        self.set_bounds(max_x=w, max_y=h)

        line_pattern = re.compile(r'(\d*)([bo$!])')
        line_data = line_pattern.findall(lines)

        line_data = [
            (1, match[1]) if match[0] == '' else (int(match[0]), match[1]) 
            for match in line_data
        ]

        c = Configuration()
        x, y = 0, 0

        for seq in line_data:
            n, act = seq
            if act == 'b':
                x += n
            elif act == 'o':
                for _ in range(n):
                    c.set_cell((x, y))
                    x += 1
            elif act == '$':
                y += n
                x = 0
            elif act == '!':
                pass # should be the last action

        self.place(c, loc=loc)
        return self
            
