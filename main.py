from game import GameOfLife, RenderType
from objects import *
import pygame

import time

pygame.init()

def main():
    g = GameOfLife(render_type=RenderType.PYGAME)

    g.load("./configs/glider.pkl")

    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    dt = 0

    ticker = 0
    tick_period = 1

    ticking = False

    ox, oy = 0, 0

    NUM_CELLS_X = 100
    cell_size = 1280 / NUM_CELLS_X
    kwargs = dict(
        screen=screen, color='white', bg_color='black'
    )

    g.render(**kwargs)

    old_pressed = {
        pygame.K_p: False,
        pygame.K_o: False,
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
            oy += 100 * dt
        if keys[pygame.K_s]:
            oy -= 100 * dt
        if keys[pygame.K_d]:
            ox -= 100 * dt
        if keys[pygame.K_a]:
            ox += 100 * dt

        if keys[pygame.K_r]:
            tick_period -= 0.1 * dt
        if keys[pygame.K_e]:
            tick_period += 0.1 * dt

        w = screen.get_width()
        h = screen.get_height()

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

        if clicked[pygame.K_RIGHT]:
            g.save(f"./configs/{int(time.time())}.pkl")
        if clicked[pygame.K_LEFT]:
            ticking = not ticking

        mouse_pressed = pygame.mouse.get_pressed()[0]
        if not mouse_old_pressed and mouse_pressed:
            x, y = pygame.mouse.get_pos()
            g.flip_cell((
                int((x - ox) / cell_size),
                int((y - oy) / cell_size),
            ))
        mouse_old_pressed = mouse_pressed

        pygame.display.flip()

        dt = clock.tick(60) / 1000

        if ticking:
            ticker += dt

if __name__ == "__main__":
    main()
