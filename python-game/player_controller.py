from camera import cam
from msg_json import read_json
from detect import box
from tiles import tile_controller

import pygame

pygame.init()

class Player:
    def __init__(self, x=0, y=0):
        self.json_path = "python-game/data/player.json"
        # jsn = read_json(self.json_path)

        # self.x = jsn["x"]
        # self.y = jsn["y"]

        self.x = x
        self.y = x
        self.speed = 2

        self.collidables = []
    
    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed
        if (self.collide()):
            self.x -= dx * self.speed
            self.y -= dy * self.speed
    
    def local_pos(self):
        lx, ly = self.x - cam.x, self.y - cam.y
        return lx, ly

    def collide(self):
        for tile in tile_controller.collision_data:
            tx, ty = tile["x"], tile["y"]
            lx, ly = self.local_pos()

            if (box(lx, ly, tx, ty)):
                return True
        
        return False
    
    def interact(self, keys):
        for tile in tile_controller.interact_data:
            tx, ty = tile["x"], tile["y"]
            lx, ly = self.local_pos()

            if (box(lx, ly, tx, ty)):
                if (keys[pygame.K_e]):
                    return True
        
        return False

player = Player()