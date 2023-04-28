from configurations import Configuration, RenderType

class GameOfLife(Configuration):
    def __init__(self, alive_cells=None, render_type=RenderType.PRINT_STATE, rule_str="b3/s23"):
        super().__init__(alive_cells=alive_cells, render_type=render_type)

        self.born = set([int(c) for c in rule_str.split("/")[0][1:]])
        self.stay = set([int(c) for c in rule_str.split("/")[1][1:]])

    def get_neighbors(self, pos):
        x, y = pos
        return set(
            (x + dx, y + dy)
            for dx in range(-1, 2)
            for dy in range(-1, 2)
            if dx != 0 or dy != 0
        )

    def count_alive_neighbors(self, pos):
        return sum(self.is_set(neighbor) for neighbor in self.get_neighbors(pos))

    def get_updatable_cells(self):
        updatable_cells = set()
        updatable_cells = updatable_cells.union(self.alive_cells)
        for cell in self.alive_cells:
            updatable_cells = updatable_cells.union(self.get_neighbors(cell))
        return updatable_cells

    def tick(self):
        cells_to_clear = []
        cells_to_set = []

        updatable_cells = self.get_updatable_cells()
        for cell in updatable_cells:
            cnt = self.count_alive_neighbors(cell)
            alive = self.is_set(cell)

            if alive:
                if cnt not in self.stay:
                    cells_to_clear.append(cell)
            else:
                if cnt in self.born:
                    cells_to_set.append(cell)

        self.clear_cells(cells_to_clear)
        self.set_cells(cells_to_set)
