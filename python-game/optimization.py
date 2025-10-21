import pygame

image_cache = {}

def get_image(path):
    if path not in image_cache:
        image_cache[path] = pygame.image.load(path).convert_alpha()
    return image_cache[path]