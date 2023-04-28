# Conway's Game of Life Simulator

Run with `python main.py`. Within the pygame window use these controls:
- Click to flip a cell
- WASD to move the "camera"
- UP to zoom in
- DOWN to zoom out
- RIGHT arrow key to play/pause the simulation
- LEFT arrow key to save the configuration to a file named by the timestamp
- E to slow down the simulation
- R to speed up the simulation
- Q to quit

To create new configurations in the code use the following methods:
- load(fname, loc=(0, 0)) will load a configuration from a pkl file (see the configs/*.pkl files) and place it in the specified location (by default 0, 0).
- load_from_lexicon(lexicon_name, loc=(0, 0)) will load a configuration from the Life Lexicon and place it in the specified location (by default 0, 0). See [https://conwaylife.com/ref/lexicon/lex.htm](https://conwaylife.com/ref/lexicon/lex.htm)
- place(config, loc=(0, 0)) will place another configuration object onto the game at location loc (by default 0, 0). This function can be used to place the objects from objects.py. For example, g.place(Block, loc=(1,2)) will place a block at (1, 2).
- Further, note that you should call shift_to_origin before placing these to ensure they are placed in the correct spot. Also, each configuration can be rotated about the origin (cw or ccw) with the rotate_cw and rotate_ccw methods. Remember to call shift_to_origin after using any rotate methods
- Lastly, to see the bounds of any configuration, call get_bounds and place everything based on these bounds to avoid overlap.