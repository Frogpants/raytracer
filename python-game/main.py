import pygame
import sys

import math as m

from tools import *
from screen_data import *

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Python Game")

clock = pygame.time.Clock()
player = pygame.Rect(half_width, half_height, 32, 32)
speed = 5

x, y = 0, 0
velocity = 0
acceleration = 0

fx, fy = 0, 0
fDir = 0
mass = 10

def applyForce(force, dir):
    fx += (force * mass) * m.sin(dir)
    fy += (force * mass) * m.cos(dir)
    fDir = dir

def move(speed):
    x += speed * m.sin(fDir)
    y += speed * m.cos(fDir)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= speed
    if keys[pygame.K_RIGHT]:
        player.x += speed
    if keys[pygame.K_UP]:
        player.y -= speed
    if keys[pygame.K_DOWN]:
        player.y += speed

    screen.fill((30, 30, 30))
    pygame.draw.rect(screen, (0, 200, 255), player)
    pygame.display.flip()
    clock.tick(60)
