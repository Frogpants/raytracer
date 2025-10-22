import pygame
import sys

from screen_data import *

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Python Game")

clock = pygame.time.Clock()

img_path = "python-game/data/images.json"