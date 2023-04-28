from game import GameOfLife, RenderType
from objects import *
import pygame
import numpy as np
import tkinter as tk
from tkinter import simpledialog
from args_util import get_args
from args import make_parser

import time

root = tk.Tk()
root.withdraw()
pygame.init()
pygame.font.init()

def main(args):
    def initialize_game(g: GameOfLife):
        g.clear()
        
        g.load(args.initial_config)

        return g

    g = GameOfLife(render_type=RenderType.PYGAME, born=args.born, stay=args.stay)

    initialize_game(g)

    screen = pygame.display.set_mode((args.width, args.height))
    pygame.display.set_icon(pygame.image.load('./res/icon.png'))
    pygame.display.set_caption("Conway's Game of Life")
    clock = pygame.time.Clock()
    running = True
    dt = 0
    generation = 0

    ticker = 0
    tick_period = 1 / args.init_tick_frequency

    ticking = False
    show_debug = False
    show_controls = False
    grid_color = args.grid_color
    loaded_object = None

    w = screen.get_width()
    h = screen.get_height()

    ox, oy = w / 2, h / 2

    cell_size = args.init_cell_size

    font = pygame.font.SysFont(args.font, args.font_size, bold=True)

    kwargs = dict(
        screen=screen, color=args.cell_color, bg_color=args.bg_color, pygame=pygame
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
                inc = args.scroll_zoom_speed * event.y
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

            grid_step = 1 if cell_size > args.grid_cell_thresh else int(args.grid_cell_thresh + 1 - cell_size)

            for i in range(start_i, end_i + 1, grid_step):
                sx = ox + i * cell_size
                pygame.draw.line(surface=screen, color=grid_color, start_pos=(sx, 0), end_pos=(sx, h))

            for j in range(start_j, end_j + 1, grid_step):
                sy = oy + j * cell_size
                pygame.draw.line(surface=screen, color=grid_color, start_pos=(0, sy), end_pos=(w, sy))

        keys = pygame.key.get_pressed()
        for k in clicked:
            clicked[k] = keys[k] and not old_pressed[k]
            old_pressed[k] = keys[k]

        if keys[pygame.K_q]:
            running = False
        
        if keys[pygame.K_w]:
            oy += args.camera_speed * dt
        if keys[pygame.K_s]:
            oy -= args.camera_speed * dt
        if keys[pygame.K_d]:
            ox -= args.camera_speed * dt
        if keys[pygame.K_a]:
            ox += args.camera_speed * dt

        if keys[pygame.K_r]:
            df = args.freq_speed * dt
            tick_period = tick_period / (1 + df * tick_period)
        if keys[pygame.K_e]:
            df = -args.freq_speed * dt
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
            grid_color = args.grid_color if grid_color is None else None
        if clicked[pygame.K_f]:
            show_debug = not show_debug
        if clicked[pygame.K_z]:
            show_controls = not show_controls
        if clicked[pygame.K_l]:
            if loaded_object is None:
                answer = simpledialog.askstring(title="Load a configuration", prompt="Please specify either a file path (txt, rle, pkl), lexicon configuration name (ex: GIG), object name (ex: objects.Block), or a url to a file.")
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
        elif keys[pygame.K_t]:
            g.clear_cell((mi, mj))
        mouse_old_pressed = mouse_pressed

        sx = ox + mi * cell_size
        sy = oy + mj * cell_size
        if loaded_object is None:
            color = args.hover_alive_color if g.is_set((mi, mj)) else args.hover_dead_color
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
            loaded_object.render(screen=screen, color=args.hover_dead_color, bg_color=None, pygame=pygame, origin=(sx, sy), cell_size=cell_size)

        if keys[pygame.K_UP]:
            inc = args.zoom_speed * dt
            new_cell_size = cell_size + inc
            ox = w / 2 - new_cell_size / cell_size * (w / 2 - ox)
            oy = h / 2 - new_cell_size / cell_size * (h / 2 - oy)
            cell_size = new_cell_size

        if keys[pygame.K_DOWN]:
            inc = -args.zoom_speed * dt
            new_cell_size = cell_size + inc
            ox = w / 2 - new_cell_size / cell_size * (w / 2 - ox)
            oy = h / 2 - new_cell_size / cell_size * (h / 2 - oy)
            cell_size = new_cell_size

        if clicked[pygame.K_LEFT] or clicked[pygame.K_KP_PLUS]:
            answer = simpledialog.askstring(title="Save the current configuration", prompt="Please specify the file name to save this configuration to. It will be saved to ./configs/{FILE NAME}.pkl.")
            if answer is not None:
                g.save(f"./configs/{answer}.pkl")
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
            y = args.text_padding
            s = "Debug Info:"
            text_surface = font.render(s, True, args.debug_color)
            screen.blit(text_surface, dest=(args.text_padding, y))
            y += args.font_size
            for k, v in debug_info.items():
                s = f"{k}: {v}"
                text_surface = font.render(s, True, args.debug_color)
                screen.blit(text_surface, dest=(2 * args.font_size + args.text_padding, y))
                y += args.font_size

        if show_controls:
            controls = {
                "click Mouse": "flip a cell",
                "hold T": "turn on eraser mode",
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
            y = h - args.text_padding - args.font_size
            for k, v in reversed(controls.items()):
                s = f"{k}: {v}"
                text_surface = font.render(s, True, args.controls_color)
                screen.blit(text_surface, dest=(2 * args.font_size + args.text_padding, y))
                y -= args.font_size
            s = "Controls:"
            text_surface = font.render(s, True, args.controls_color)
            screen.blit(text_surface, dest=(args.text_padding, y))

        pygame.display.flip()

        dt = clock.tick(args.framerate) / 1000

        if ticking:
            ticker += dt

if __name__ == "__main__":
    args = get_args(make_parser(), configs_root="./run_config")
    main(args)
