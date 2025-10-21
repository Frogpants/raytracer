import pygame

pygame.init()

info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
half_width, half_height = screen_width/2, screen_height/2

def set_screen_size(w, h):
    screen_width, screen_height = w, h
    half_width, half_height = w/2, h/2