from screen_data import half_width, half_height

import pygame

pygame.init()

# module-level mouse state; other modules should import the module and
# reference these variables (e.g. `import mouse_data; mouse_data.mouse_x`)
mouse_down = False

# initialize mouse position adjusted to screen center
mouse_x, mouse_y = pygame.mouse.get_pos()
mouse_x -= half_width
mouse_y -= half_height

def get_mouse():
    """Update module-level mouse_x and mouse_y adjusted by half-width/height.

    Call this each frame from the main loop (e.g. `mouse_data.get_mouse()`).
    """
    global mouse_x, mouse_y
    mx, my = pygame.mouse.get_pos()
    mouse_x = mx
    mouse_y = my