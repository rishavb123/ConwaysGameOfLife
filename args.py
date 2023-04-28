import argparse

INITIAL_CONFIG = "objects.GliderGun"
BORN_STR = '3'
STAY_STR = '23'

WIDTH = 1920
HEIGHT = 1080

INIT_CELL_SIZE = 20
COLOR = 'white'
BG_COLOR = 'black'
GRID_CELL_THRESH = 10
GRID_COLOR = '#222222'
HOVER_ALIVE = '#cccccc'
HOVER_DEAD = '#333333'

FONT = 'Courier New'
FONT_SIZE = 20
DEBUG_COLOR = '#00ff00'
CONTROLS_COLOR = '#ff00ff'
TEXT_PADDING = 5

INIT_TICK_FREQ = 3
MAX_FRAME_RATE = 60

CAMERA_SPEED = 200
FREQ_SPEED = 1.5
ZOOM_SPEED = 10
SCROLL_ZOOM_SPEED = 2

def make_parser():
    parser = argparse.ArgumentParser(description="Run the conway's game of life simulator")

    parser.add_argument("--initial-config", "-ic", type=str, default=INITIAL_CONFIG, help="The initial configuration to load into the simulator.")
    parser.add_argument("--born", "-b", type=str, default=BORN_STR, help="The number of neighbors to cause a dead cell to become alive")
    parser.add_argument("--stay", "-s", type=str, default=STAY_STR, help="The number of neighbors to cause a alive cell to stay alive")

    parser.add_argument("--width", "-sw", type=int, default=WIDTH, help="The window width in pixels")
    parser.add_argument("--height", "-sh", type=int, default=HEIGHT, help="The window height in pixels")

    parser.add_argument("--init-cell-size", "-cs", type=float, default=INIT_CELL_SIZE, help="The initial cell size")
    parser.add_argument("--cell-color", "-cc", type=str, default=COLOR, help="The color of the cells")
    parser.add_argument("--bg-color", "-bc", type=str, default=BG_COLOR, help="The background color")
    parser.add_argument("--grid-cell-thresh", "-t", type=float, default=GRID_CELL_THRESH, help="The cell size threshold to start reducing the number of grid lines")
    parser.add_argument("--grid-color", type=str, default=GRID_COLOR, help="The color of the grid lines")
    parser.add_argument("--hover-alive-color", "-ha", type=str, default=HOVER_ALIVE, help="The color to use when hovering over an alive cell")
    parser.add_argument("--hover-dead-color", "-hd", type=str, default=HOVER_DEAD, help="The color to use when hovering over a dead cell")
    
    parser.add_argument('--font', '-f', type=str, default=FONT, help="The font to display text with")
    parser.add_argument('--font-size', '-fs', type=int, default=FONT_SIZE, help="The font size to display text with")
    parser.add_argument("--debug-color", '-d', type=str, default=DEBUG_COLOR, help="The color of the debug message shown once F is clicked.")
    parser.add_argument("--controls-color", '-z', type=str, default=CONTROLS_COLOR, help="The color of the debug message shown once Z is clicked")
    parser.add_argument('--text-padding', '-p', type=int, default=TEXT_PADDING, help="The number of pixels to pad the text width from the edge of the window")

    parser.add_argument("--init-tick-frequency", '-tf', type=float, default=INIT_TICK_FREQ, help="The initial tick frequency of the simulation (in ticks per second)")
    parser.add_argument("--framerate", "-fr", type=int, default=MAX_FRAME_RATE, help="The maximum number of frame per second to render. This also caps the tick frequency")

    parser.add_argument("--camera-speed", '-cm', type=int, default=CAMERA_SPEED, help="The camera speed to move at in each direction (in pixels per second)")
    parser.add_argument("--freq-speed", '-fq', type=float, default=FREQ_SPEED, help="The speed at which to change the tick frequency (in ticks per second per second)")
    parser.add_argument("--zoom-speed", '-zs', type=float, default=ZOOM_SPEED, help="The speed at which to change the cell size (in pixels per second)")
    parser.add_argument("--scroll-zoom-speed", '-sz', type=float, default=SCROLL_ZOOM_SPEED, help="The speed at which to change the cell size from the mouse scroll wheel (in pixels per second)")

    return parser
