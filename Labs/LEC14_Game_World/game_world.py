
world = [[],[]]

def add_object(o,depth):
    world[depth].append(o)

def add_objests(ol,depth):
    world[depth]+=ol


def update():
    for layer in world:
        for o in layer:
            o.update()

def render():
    for layer in world:
        for o in layer:
            o.draw()

def remove(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            return