from game import GameOfLife, RenderType
from objects import *
import pygame
import numpy as np

import time

pygame.init()
pygame.font.init()

def initialize_game_dev(g: GameOfLife):
    g.clear()

    g.load("https://copy.sh/life/examples/101.rle")

    return g

# TODO: add argparser

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
    show_debug = False

    ox, oy = screen.get_width() / 2, screen.get_height() / 2

    NUM_CELLS_X = 100
    cell_size = 1280 / NUM_CELLS_X
    GRID_COLOR = '#222222'
    TEXT_COLOR = '#00ff00'
    FONT_SIZE = 20

    font = pygame.font.SysFont('Courier New', FONT_SIZE, bold=True)

    kwargs = dict(
        screen=screen, color='white', bg_color='black', pygame=pygame, grid_color=GRID_COLOR
    )

    g.render(**kwargs)

    old_pressed = {
        pygame.K_LEFT: False,
        pygame.K_RIGHT: False,
        pygame.K_c: False,
        pygame.K_x: False,
        pygame.K_g: False,
        pygame.K_KP_ENTER: False,
        pygame.K_KP_PLUS: False,
        pygame.K_f: False,
    }
    clicked = {
        **old_pressed
    }

    mouse_old_pressed = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEWHEEL:
                inc = 2 * event.y
                new_cell_size = cell_size + inc
                ox = w / 2 - new_cell_size / cell_size * (w / 2 - ox)
                oy = h / 2 - new_cell_size / cell_size * (h / 2 - oy)
                cell_size = new_cell_size

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
        if clicked[pygame.K_f]:
            show_debug = not show_debug

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

        if clicked[pygame.K_LEFT] or clicked[pygame.K_KP_PLUS]:
            g.save(f"./configs/{int(time.time())}.pkl")
        if clicked[pygame.K_RIGHT] or clicked[pygame.K_KP_ENTER]:
            ticking = not ticking

        if show_debug:
            debug_info = {
                'frame_rate': f"{1/dt:0.4f}",
                'cell_size': f"{cell_size:0.2f}",
                'origin': f"({ox:0.2f}, {oy:0.2f})",
                'grid_color': kwargs["grid_color"],
                'width': w,
                'height': h,
                'ticking': ticking,
                'tick_freq': f"{1 / tick_period:0.4f}"
            }
            y = 5
            s = "Debug Info:"
            text_surface = font.render(s, True, TEXT_COLOR)
            screen.blit(text_surface, dest=(5, y))
            y += FONT_SIZE
            for k, v in debug_info.items():
                s = f"{k}: {v}"
                text_surface = font.render(s, True, TEXT_COLOR)
                screen.blit(text_surface, dest=(2 * FONT_SIZE + 5, y))
                y += FONT_SIZE

        pygame.display.flip()

        dt = clock.tick(60) / 1000

        if ticking:
            ticker += dt

if __name__ == "__main__":
    main()
