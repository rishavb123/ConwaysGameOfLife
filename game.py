from configurations import Configuration, RenderType

class GameOfLife(Configuration):
    def __init__(self, render_type=RenderType.PRINT_STATE):
        super().__init__(render_type)

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
                if cnt != 2 and cnt != 3:
                    cells_to_clear.append(cell)
            else:
                if cnt == 3:
                    cells_to_set.append(cell)

        self.clear_cells(cells_to_clear)
        self.set_cells(cells_to_set)
