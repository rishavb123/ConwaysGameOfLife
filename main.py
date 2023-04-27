from game import GameOfLife


def main():
    g = GameOfLife()

    g.set_cells([(0, 0), (0, 1), (0, -1)])

    g.render()

    while len(input()) == 0:
        g.tick()
        g.render()


if __name__ == "__main__":
    main()
