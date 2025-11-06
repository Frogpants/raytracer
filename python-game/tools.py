import math as m

def distance(x1, y1, x2, y2):
    dx, dy = (x2 - x1), (y2 - y1)
    return m.sqrt(dx**2, dy**2)

def point_at(x1, y1, x2, y2):
    dx, dy = (x2 - x1), (y2 - y1)
    return m.atan2(dy, dx)

def snap(val, size):
    return m.floor(val / size) * size
