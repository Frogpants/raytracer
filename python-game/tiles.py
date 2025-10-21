from tools import snap
from camera import cam
from detect import on_screen
from optimization import get_image
from msg_json import read_json, update_json
from setup import screen
from mouse_data import mouse_x, mouse_y, mouse_down
from editor import tile_data

import pygame

pygame.init()

class Tiles:
    def __init__(self):
        self.tile_data = []
        self.collision_data = []
        self.interact_data = []
        self.json_path = "python-game/data/tiles.json"
    
    def tile_package(self, x=0, y=0, type=0, collidable=False, interactable=False, layer=1):
        return {"x": x, "y": y, "type": type, "collidable": collidable, "interactable": interactable, "layer": layer}
    
    def add_tile(self, x=0, y=0, type=0, collidable=False, interactable=False, layer=1):
        nx, ny = snap(x, 32), snap(y, 32)
        package = self.tile_package(nx, ny, type, collidable, interactable, layer)
        self.tile_data.append(package)

    def render_layer(self, n=1):
        self.collision_data = []
        for tile in self.tiles:
            id = self.tiles.index(tile)
            tx, ty = tile["x"] - cam.x, tile["y"] - cam.y
            img = list(read_json(self.json_path))
            img = img[tile["type"]]
            if (on_screen(tx, ty)):
                screen.blit(get_image(img), (tx, ty))
                if (tile["collidable"]):
                    package = self.tile_package(tx, ty)
                    self.collision_data.append(package)
                if (tile["interactable"]):
                    package = self.tile_package(tx, ty)
                    self.interact_data.append(package)
    
    def editor(self):
        tx, ty = snap(mouse_x + cam.x, 32) + cam.x, snap(mouse_y + cam.y, 32) + cam.y
        img = list(read_json(self.json_path))
        img = img[tile_data["type"]]
        screen.blit(get_image(img), (tx, ty))
        if (mouse_down):
            self.add_tile(tile_data)
            update_json(self.json_path, self.tile_data)

tile_controller = Tiles()
