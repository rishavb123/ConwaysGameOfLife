class Configuration:

    def __init__(self):
        self.alive_cells = set()

    def set_cell(self, pos):
        self.alive_cells.add(pos)

    def clear_cell(self, pos):
        if pos in self.alive_cells:
            self.alive_cells.remove(pos)

    def set_cells(self, pos_arr):
        [self.set_cell(pos) for pos in pos_arr]

    def clear_cells(self, pos_arr):
        [self.clear_cell(pos) for pos in pos_arr]

    def is_set(self, pos):
        return pos in self.alive_cells

    def place(self, config, loc=(0, 0)):
        if type(config) == function:
            config = config()
        self.set_cells([(cell[0] + loc[0], cell[1] + loc[1]) for cell in config.alive_cells])

    def render(self):
        print("State:", self.alive_cells)