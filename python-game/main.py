import pygame
import sys

import math as m

from tools import *
from screen_data import *
from player_controller import player
from tiles import tile_controller
from camera import cam

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Nomori")

clock = pygame.time.Clock()
player_rect = pygame.Rect(player.x, player.y, 32, 32)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    dx, dy = 0, 0
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        dx, dy = -1, 0
    if keys[pygame.K_RIGHT]:
        dx, dy = 1, 0
    if keys[pygame.K_UP]:
        dx, dy = 0, -1
    if keys[pygame.K_DOWN]:
        dx, dy = 0, 1
    
    player.move(dx, 0)
    player.move(0, dy)

    player_rect.x, player_rect.y = player.x, player.y
    screen.fill((30, 30, 30))
    pygame.draw.rect(screen, (0, 200, 255), player_rect)
    pygame.display.flip()
    clock.tick(60)
