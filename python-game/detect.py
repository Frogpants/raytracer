import math as m
from tools import distance
from screen_data import *

def box(x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    if (abs(dx) <= 64):
        if (abs(dy) <= 64):
            return True
    return False

def circle(x1, y1, x2, y2):
    dist = distance(x1, y1, x2, y2)
    if (dist <= 64):
        return True
    return False

def on_screen(x, y):
    if (abs(x) <= half_width):
        if (abs(y) <= half_height):
            return True
    return False

