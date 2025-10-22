from screen_data import half_width, half_height

import pygame

pygame.init()

mouse_down = False

mouse_x, mouse_y = pygame.mouse.get_pos()

def get_mouse():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_x -= half_width
    mouse_y -= half_height