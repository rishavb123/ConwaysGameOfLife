from game import GameOfLife, RenderType
from objects import *
import pygame
import numpy as np
import tkinter as tk
from tkinter import simpledialog

import time

root = tk.Tk()
root.withdraw()
pygame.init()
pygame.font.init()

def initialize_game_dev(g: GameOfLife):
    g.clear()

    # g.load("https://copy.sh/life/examples/101.rle")
    
    # g.place(GliderGun(), loc=(0, 0))
    # g.place(GliderGun().flip_over_x(), loc=(0, 30))

    g.load('objects.GliderGun')

    # g.load('./configs/rendal-attic/memcell.txt')

    # g.load('./configs/saved/double_glider.pkl')

    return g

# TODO: add argparser

def main(initialize_game=initialize_game_dev):
    g = GameOfLife(render_type=RenderType.PYGAME)

    initialize_game(g)

    WIDTH = 1920
    HEIGHT = 1080
    INIT_CELL_SIZE = 19.2
    GRID_COLOR = '#222222'
    DEBUG_COLOR = '#00ff00'
    CONTROLS_COLOR = '#ff00ff'
    HOVER_ALIVE = '#cccccc'
    HOVER_DEAD = '#333333'
    COLOR = 'white'
    BG_COLOR = 'black'
    FONT_SIZE = 20
    FONT = 'Courier New'
    INIT_TICK_FREQ = 3
    MAX_FRAME_RATE = 60

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    running = True
    dt = 0
    generation = 0

    ticker = 0
    tick_period = 1 / INIT_TICK_FREQ

    ticking = False
    show_debug = False
    show_controls = False
    grid_color = GRID_COLOR
    loaded_object = None

    w = screen.get_width()
    h = screen.get_height()

    ox, oy = w / 2, h / 2

    cell_size = INIT_CELL_SIZE

    font = pygame.font.SysFont(FONT, FONT_SIZE, bold=True)

    kwargs = dict(
        screen=screen, color=COLOR, bg_color=BG_COLOR, pygame=pygame
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
        pygame.K_z: False,
        pygame.K_l: False,
        pygame.K_k: False,
        pygame.K_j: False,
        pygame.K_o: False,
        pygame.K_i: False,
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
            generation += 1
            g.tick()
            ticker = 0

        g.render(**kwargs, origin=(ox, oy), cell_size=cell_size)
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
            generation = 0
        if clicked[pygame.K_x]:
            initialize_game(g)
            ticking = False
            generation = 0
        if clicked[pygame.K_g]:
            grid_color = GRID_COLOR if grid_color is None else None
        if clicked[pygame.K_f]:
            show_debug = not show_debug
        if clicked[pygame.K_z]:
            show_controls = not show_controls
        if clicked[pygame.K_l]:
            if loaded_object is None:
                answer = simpledialog.askstring(title="Load a configuration", prompt="Please specify either a file path (txt, rle, pkl), lexicon configuration name (ex: GIG), object name (ex: objects.Block), or a url to a file.")
                root.update_idletasks()
                if answer is not None:
                    try:
                        loaded_object = Configuration().load(answer).shift_to_origin().set_render_type(render_type=RenderType.PYGAME)
                    except:
                        tk.messagebox.showerror(title="Load Error", message=f"Error during loading of {answer} configuration.")
            else:
                loaded_object = None

        mx, my = pygame.mouse.get_pos()
        mi = int(np.floor((mx - ox) / cell_size))
        mj = int(np.floor((my - oy) / cell_size))

        mouse_pressed = pygame.mouse.get_pressed()[0]
        if not mouse_old_pressed and mouse_pressed:
            if loaded_object is None:
                g.flip_cell((mi, mj))
            else:
                g.place(loaded_object, loc=(mi, mj))
        mouse_old_pressed = mouse_pressed

        sx = ox + mi * cell_size
        sy = oy + mj * cell_size
        if loaded_object is None:
            color = HOVER_ALIVE if g.is_set((mi, mj)) else HOVER_DEAD
            pygame.draw.rect(surface=screen, color=color, rect=(sx, sy, cell_size, cell_size), )
        else:
            if clicked[pygame.K_k] or clicked[pygame.K_j] or clicked[pygame.K_o] or clicked[pygame.K_i]:
                if clicked[pygame.K_k]:
                    loaded_object.flip_over_x()
                if clicked[pygame.K_j]:
                    loaded_object.flip_over_y()
                if clicked[pygame.K_o]:
                    loaded_object.rotate_cw()
                if clicked[pygame.K_i]:
                    loaded_object.rotate_ccw()
                loaded_object.shift_to_origin()
            loaded_object.render(screen=screen, color=HOVER_DEAD, bg_color=None, pygame=pygame, origin=(sx, sy), cell_size=cell_size)

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
                'generation': generation,
                'frame_rate': f"{1/dt:0.4f}",
                'cell_size': f"{cell_size:0.2f}",
                'origin': f"({ox:0.2f}, {oy:0.2f})",
                'grid lines': grid_color is not None,
                'width': w,
                'height': h,
                'ticking': ticking,
                'tick_freq': f"{1 / tick_period:0.4f}",
                'mouse_pos': f"({mx:0.2f}, {my:0.2f})",
                'mouse_idx':  f"({mi:0.2f}, {mj:0.2f})",
                'loaded_object': loaded_object is not None,
            }
            y = 5
            s = "Debug Info:"
            text_surface = font.render(s, True, DEBUG_COLOR)
            screen.blit(text_surface, dest=(5, y))
            y += FONT_SIZE
            for k, v in debug_info.items():
                s = f"{k}: {v}"
                text_surface = font.render(s, True, DEBUG_COLOR)
                screen.blit(text_surface, dest=(2 * FONT_SIZE + 5, y))
                y += FONT_SIZE

        if show_controls:
            controls = {
                "click Mouse": "flip a cell",
                "hold WASD": "move the camera",
                "hold UP / MouseWheel UP": "zoom in",
                "hold DOWN / MouseWheel DOWN": "zoom out",
                "click RIGHT / ENTER": "play/pause the simulation",
                "click LEFT / PLUS": "save the configuration to file",
                "hold E": "slow simulation tick frequency",
                "hold R": "speed up simulation tick frequency",
                "click C": "clear game board",
                "click X": "reinitialize game board",
                "click L": "load  or unload a configuration",
                "click K": "flip loaded object across the x axis",
                "click J": "flip loaded object across the y axis",
                "click O": "rotate loaded object cw",
                "click I": "rotate loaded object ccw",
                "click G": "toggle grid lines",
                "click F": "show debug info",
                "click Z": "show these controls",
                "click Q": "quit"
            }
            y = h - 5 - FONT_SIZE
            for k, v in reversed(controls.items()):
                s = f"{k}: {v}"
                text_surface = font.render(s, True, CONTROLS_COLOR)
                screen.blit(text_surface, dest=(2 * FONT_SIZE + 5, y))
                y -= FONT_SIZE
            s = "Controls:"
            text_surface = font.render(s, True, CONTROLS_COLOR)
            screen.blit(text_surface, dest=(5, y))

        pygame.display.flip()

        dt = clock.tick(MAX_FRAME_RATE) / 1000

        if ticking:
            ticker += dt

if __name__ == "__main__":
    main()
