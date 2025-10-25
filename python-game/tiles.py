from tools import snap
from camera import cam
from detect import on_screen
from optimization import get_image
from msg_json import read_json, update_json
from setup import screen, img_path
from mouse_data import mouse_x, mouse_y, mouse_down
from editor import tile_data
from screen_data import half_width, half_height

import pygame

pygame.init()

class Tiles:
    def __init__(self):
        self.tile_data = []
        self.collision_data = []
        self.interact_data = []
        self.json_path = "python-game/data/tiles.json"

        self.img_data = list(read_json(img_path))
    
    def tile_package(self, x=0, y=0, type=0, collidable=False, interactable=False, layer=1):
        return {"x": x, "y": y, "type": type, "collidable": collidable, "interactable": interactable, "layer": layer}
    
    def add_tile(self, x=0, y=0, type=0, collidable=False, interactable=False, layer=1):
        package = self.tile_package(x, y, type, collidable, interactable, layer)
        self.tile_data.append(package)

    def render_layer(self, n=1):
        self.collision_data = []
        for tile in self.tile_data:
            tx, ty = tile["x"] - cam.x, tile["y"] - cam.y
            img = self.img_data[tile["type"]]
            # if (on_screen(tx, ty)):
            screen.blit(get_image(img), (tx, ty))
            if (tile["collidable"]):
                package = self.tile_package(tx, ty)
                self.collision_data.append(package)
            if (tile["interactable"]):
                package = self.tile_package(tx, ty)
                self.interact_data.append(package)
    
    def editor(self):
        tx, ty = snap(mouse_x + cam.x, 32) - cam.x, snap(mouse_y + cam.y, 32) - cam.y
        img = "python-game/imgs/tile1.png"
        # screen.blit(get_image(img), (tx, ty))
        pygame.draw.rect(screen, (0, 200, 255), )
        if mouse_down:
            tile_data["x"] = tx + cam.x
            tile_data["y"] = ty + cam.y
            self.add_tile(**tile_data)
            update_json(self.json_path, self.tile_data)

tile_controller = Tiles()
