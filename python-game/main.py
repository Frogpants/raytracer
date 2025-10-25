import pygame
import sys

import math as m

from tools import *
from screen_data import *
import mouse_data
from player_controller import player
from tiles import tile_controller
from camera import cam
from setup import screen
from msg_json import update_json

pygame.init()
pygame.display.set_caption("Nomori")

clock = pygame.time.Clock()
player_rect = pygame.Rect(player.x, player.y, 32, 32)

editor = False

tile_controller.add_tile()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            update_json("python-game/data/tiles.json", [])
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_data.mouse_down = True
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_data.mouse_down = False
    
    # update mouse position and then clear screen before rendering
    mouse_data.get_mouse()
    screen.fill((30, 30, 30))

    tile_controller.render_layer()

    keys = pygame.key.get_pressed()

    if (keys[pygame.K_LALT] and keys[pygame.K_e]):
        editor = True
    elif (keys[pygame.K_LALT] and keys[pygame.K_r]):
        editor = False

    dx, dy = 0, 0
    
    if (editor):
        tile_controller.editor()
        if keys[pygame.K_a]:
            cam.x += -4
        if keys[pygame.K_d]:
            cam.x += 4
        if keys[pygame.K_w]:
            cam.y += -4
        if keys[pygame.K_s]:
            cam.y += 4
    else:
        if keys[pygame.K_a]:
            dx, dy = -1, 0
        if keys[pygame.K_d]:
            dx, dy = 1, 0
        if keys[pygame.K_w]:
            dx, dy = 0, -1
        if keys[pygame.K_s]:
            dx, dy = 0, 1
        cam.follow(player.x, player.y)
    
    player.move(dx, 0)
    player.move(0, dy)

    player_rect.x, player_rect.y = player.local_pos()
    player_rect.x += half_width
    player_rect.y += half_height
    pygame.draw.rect(screen, (0, 200, 255), player_rect)
    pygame.display.flip()
    clock.tick(60)
