import pygame

pygame.init()

mouse_down = pygame.MOUSEBUTTONDOWN

mouse_x, mouse_y = pygame.mouse.get_pos()

def get_mouse():
    mouse_x, mouse_y = pygame.mouse.get_pos()