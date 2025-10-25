import pygame

pygame.init()

info = pygame.display.Info()
# prefer ints for pixel coordinates
screen_width, screen_height = int(info.current_w), int(info.current_h)
half_width, half_height = screen_width // 2, screen_height // 2

def set_screen_size(w, h):
    global screen_width, screen_height, half_width, half_height
    screen_width, screen_height = int(w), int(h)
    half_width, half_height = screen_width // 2, screen_height // 2