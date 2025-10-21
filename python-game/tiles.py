from tools import snap
from camera import cam
from detect import on_screen
from optimization import get_image
from msg_json import read_json
from setup import screen
from mouse_data import mouse_x, mouse_y

import pygame

class Tiles:
    def __init__(self):
        self.tile_data = []
        self.collision_data = []
        self.json_path = "python-game/data/tiles.json"
    
    def tile_package(self, x=0, y=0, type=0, collideable=False, interactable=False, layer=1):
        return {"x": x, "y": y, "type": type, "collideable": collideable, "interactable": interactable, "layer": layer}
    
    def add_tile(self, x=0, y=0, type=0, collideable=False, interactable=False, layer=1):
        nx, ny = snap(x, 32), snap(y, 32)
        package = self.tile_package(nx, ny, type, collideable, interactable, layer)
        self.tile_data.append(package)

    def render_layer(self, n=1):
        self.collision_data = []
        for tile in self.tiles:
            id = self.tiles.index(tile)
            tx, ty = tile["x"] - cam.x, tile["y"] - cam.y
            if (on_screen(tx, ty)):
                screen.blit(get_image("sprites/enemy_01.png"), (tx, ty))
                if (tile.collideable):
                    package = self.tile_package(tx, ty)
                    self.collision_data.append(package)
    
    def editor(self):
        tx, ty = snap(mouse_x + cam.x, 32) + cam.x, snap(mouse_y + cam.y, 32) + cam.y,
        

