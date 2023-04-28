from game import GameOfLife, RenderType
from objects import *
import pygame
import numpy as np

import time

pygame.init()

def initialize_game_dev(g: GameOfLife):
    g.clear()

    g.load_from_lexicon("gourmet")

    return g

def main(initialize_game=initialize_game_dev):
    g = GameOfLife(render_type=RenderType.PYGAME)

    initialize_game(g)

    screen = pygame.display.set_mode((1920, 1080))
    clock = pygame.time.Clock()
    running = True
    dt = 0

    ticker = 0
    tick_freq = 3
    tick_period = 1 / tick_freq

    ticking = False

    ox, oy = screen.get_width() / 2, screen.get_height() / 2

    NUM_CELLS_X = 100
    cell_size = 1280 / NUM_CELLS_X
    GRID_COLOR = '#222222'

    kwargs = dict(
        screen=screen, color='white', bg_color='black', pygame=pygame, grid_color=GRID_COLOR
    )

    g.render(**kwargs)

    old_pressed = {
        pygame.K_LEFT: False,
        pygame.K_RIGHT: False,
        pygame.K_c: False,
        pygame.K_x: False,
        pygame.K_g: False
    }
    clicked = {
        **old_pressed
    }

    mouse_old_pressed = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if ticker > tick_period and ticking:
            g.tick()
            ticker = 0

        g.render(**kwargs, origin=(ox, oy), cell_size=cell_size)

        keys = pygame.key.get_pressed()
        for k in clicked:
            clicked[k] = keys[k] and not old_pressed[k]
            old_pressed[k] = keys[k]

        if keys[pygame.K_q]:
            running = False
        
        if keys[pygame.K_w]:
            oy += 200 * dt
        if keys[pygame.K_s]:
            oy -= 200 * dt
        if keys[pygame.K_d]:
            ox -= 200 * dt
        if keys[pygame.K_a]:
            ox += 200 * dt

        if keys[pygame.K_r]:
            df = 1.5 * dt
            tick_period = tick_period / (1 + df * tick_period)
        if keys[pygame.K_e]:
            df = -1.5 * dt
            tick_period = tick_period / (1 + df * tick_period)

        if clicked[pygame.K_c]:
            g.clear()
            ticking = False
        if clicked[pygame.K_x]:
            initialize_game(g)
            ticking = False
        if clicked[pygame.K_g]:
            kwargs["grid_color"] = GRID_COLOR if kwargs["grid_color"] is None else None

        w = screen.get_width()
        h = screen.get_height()

        mouse_pressed = pygame.mouse.get_pressed()[0]
        if not mouse_old_pressed and mouse_pressed:
            x, y = pygame.mouse.get_pos()
            g.flip_cell((
                int(np.floor((x - ox) / cell_size)),
                int(np.floor((y - oy) / cell_size)),
            ))
        else:
            x, y = pygame.mouse.get_pos()
            i = int(np.floor((x - ox) / cell_size))
            j = int(np.floor((y - oy) / cell_size))
            sx = ox + i * cell_size
            sy = oy + j * cell_size
            color = '#cccccc' if g.is_set((i, j)) else '#333333'
            pygame.draw.rect(surface=screen, color=color, rect=(sx, sy, cell_size, cell_size), )
        mouse_old_pressed = mouse_pressed

        if keys[pygame.K_UP]:
            inc = 10 * dt
            new_cell_size = cell_size + inc
            ox = w / 2 - new_cell_size / cell_size * (w / 2 - ox)
            oy = h / 2 - new_cell_size / cell_size * (h / 2 - oy)
            cell_size = new_cell_size

        if keys[pygame.K_DOWN]:
            inc = -10 * dt
            new_cell_size = cell_size + inc
            ox = w / 2 - new_cell_size / cell_size * (w / 2 - ox)
            oy = h / 2 - new_cell_size / cell_size * (h / 2 - oy)
            cell_size = new_cell_size

        if clicked[pygame.K_LEFT]:
            g.save(f"./configs/{int(time.time())}.pkl")
        if clicked[pygame.K_RIGHT]:
            ticking = not ticking

        pygame.display.flip()

        dt = clock.tick(60) / 1000

        if ticking:
            ticker += dt

if __name__ == "__main__":
    main()
