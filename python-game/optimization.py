import pygame

image_cache = {}

def get_image(path):
    if path not in image_cache:
        image_cache[path] = pygame.image.load(path).convert_alpha()
    return image_cache[path]

def get_rect(x, y):
    return pygame.Rect(x, y, 32, 32)