import math as m
from tools import distance
from screen_data import *

def box(x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    if (m.abs(dx) <= 64):
        if (m.abs(dy) <= 64):
            return 1
    return 0

def circle(x1, y1, x2, y2):
    dist = distance(x1, y1, x2, y2)
    if (dist <= 64):
        return 1
    return 0

def on_screen(x, y):
    if (m.abs(x) <= half_width):
        if (m.abs(y) <= half_height):
            return 1
    return 0

