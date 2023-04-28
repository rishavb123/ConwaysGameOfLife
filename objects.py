from configurations import Configuration

def GOL_Object(cells):
    if callable(cells):
        return lambda: GOL_Object(cells())
    
    c = Configuration()
    c.set_cells(cells)
    return c

def CompoundGOL_Object(objects):
    if callable(objects):
        return lambda: CompoundGOL_Object(objects())

    c = Configuration()
    for k, v in objects.items():
        c.place(v, loc=k)
    return c

@GOL_Object
def Block():
    return [
        (0, 0),
        (1, 0),
        (0, 1),
        (1, 1),
    ]

@GOL_Object
def Boat():
    return [
        (0, 0),
        (0, 1),
        (1, 0),
        (1, 2),
        (2, 1)
    ]

@GOL_Object
def Loaf():
    return [
        (1, 0),
        (2, 0),
        (0, 1),
        (0, 2),
        (1, 3),
        (2, 2),
        (3, 1),
    ]

@GOL_Object
def Ship():
    return [
        (0, 0),
        (1, 0),
        (0, 1),
        (2, 1),
        (2, 2),
        (1, 2)
    ]

@GOL_Object
def HBar():
    return [
        (0, 0),
        (1, 0),
        (2, 0)
    ]

@GOL_Object
def VBar():
    return [
        (0, 0),
        (0, 1),
        (0, 2)
    ]

@CompoundGOL_Object
def Glider():
    return {
        (0, 2): HBar,
        (0, 0): GOL_Object([
            (1, 0), (2, 1)
        ])
    }

@CompoundGOL_Object
def SpaceShip():
    return {
        (0, 1): VBar,
        (1, 3): HBar,
        (0, 0): GOL_Object([
            (1, 0), (4, 0), (4, 2)
        ])
    }


@GOL_Object
def Cat():
    return [
        (0, 5),
        (1, 5),
        (2, 3),
        (2, 5),
        (2, 9),
        (3, 3),
        (3, 5),
        (3, 8),
        (4, 1),
        (4, 2),
        (4, 3),
        (4, 4),
        (4, 5),
        (4, 7),
        (5, 0),
        (5, 6),
        (6, 1),
        (6, 4),
        (6, 7),
        (7, 2),
        (7, 7),
        (8, 2),
        (8, 5),
        (8, 7),
        (9, 2),
        (9, 7),
        (10, 1),
        (10, 4),
        (10, 7),
        (11, 0),
        (11, 6),
        (12, 1),
        (12, 2),
        (12, 3),
        (12, 4),
        (12, 5),
        (12, 7),
        (13, 3),
        (13, 5),
        (13, 8),
        (14, 3),
        (14, 5),
        (14, 9),
        (15, 5),
        (16, 5)
    ]


@GOL_Object
def GliderGun():
    return [
        (0, 4),
        (0, 5),
        (1, 4),
        (1, 5),
        (10, 4),
        (10, 5),
        (10, 6),
        (11, 3),
        (11, 7),
        (12, 2),
        (12, 8),
        (13, 2),
        (13, 8),
        (14, 5),
        (15, 3),
        (15, 7),
        (16, 4),
        (16, 5),
        (16, 6),
        (17, 5),
        (20, 2),
        (20, 3),
        (20, 4),
        (21, 2),
        (21, 3),
        (21, 4),
        (22, 1),
        (22, 5),
        (24, 0),
        (24, 1),
        (24, 5),
        (24, 6),
        (34, 2),
        (34, 3),
        (35, 2),
        (35, 3)
    ]