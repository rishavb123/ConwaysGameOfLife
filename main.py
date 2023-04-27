from game import GameOfLife
from objects import *

def main():
    g = GameOfLife()

    g.place(Glider)

    g.render()

    while len(input()) == 0:
        g.tick()
        g.render()


if __name__ == "__main__":
    main()
