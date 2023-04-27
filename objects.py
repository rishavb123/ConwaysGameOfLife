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
def Box():
    return [
        (0, 0),
        (1, 0),
        (0, 1),
        (1, 1),
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