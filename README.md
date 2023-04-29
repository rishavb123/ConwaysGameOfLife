# Conway's Game of Life Simulator

Dependencies:
- pygame
- numpy
- re
- argparse
- pickle
- enum
- validators
- urllib
- tkinter
- PyYaml

Run with `python main.py`. Run `python main.py -h` to see the runtime configurations that can be used through command line arguments or a yml or json file in the run_config folder to specify runtime parameters. Once a runtime configuration is create, it can be used using `python main.py -c FILE_NAME`.


Within the pygame window use these controls:
- Click to flip a cell
- T to turn on eraser mode
- WASD to move the "camera"
- UP (or MOUSEWHEEL) to zoom in
- DOWN (or MOUSEWHEEL) to zoom out
- SPACE (or V) to manually tick the simulation
- RIGHT (or ENTER) arrow key to play/pause the simulation
- LEFT (or PLUS) arrow key to save the configuration to a file
- E to slow down the simulation
- R to speed up the simulation
- C to clear the game board
- X to reinitialize the board
- L to load or unload an object
- K: flip loaded object across the x axis
- J: flip loaded object across the y axis
- O: rotate loaded object cw
- I: rotate loaded object ccw
- G to turn off or on grid lines
- F to show debug info
- Z to show controls
- Q to quit

These controls can be viewed in game by clicking the z key.

To create new configurations in the code use the following methods:
- load_from_pkl(fname, loc=(0, 0)) will load a configuration from a pkl file (see the configs/*.pkl files) and place it in the specified location (by default 0, 0).
- load_from_lexicon(lexicon_name, loc=(0, 0)) will load a configuration from the Life Lexicon and place it in the specified location (by default 0, 0). See [https://conwaylife.com/ref/lexicon/lex.htm](https://conwaylife.com/ref/lexicon/lex.htm)
- place(config, loc=(0, 0)) will place another configuration object onto the game at location loc (by default 0, 0). This function can be used to place the objects from objects.py. For example, g.place(Block, loc=(1,2)) will place a block at (1, 2).
- Further, note that you should call shift_to_origin before placing these to ensure they are placed in the correct spot. Also, each configuration can be rotated about the origin (cw or ccw) with the rotate_cw and rotate_ccw methods. Remember to call shift_to_origin after using any rotate methods
- Lastly, to see the bounds of any configuration, call get_bounds and place everything based on these bounds to avoid overlap.