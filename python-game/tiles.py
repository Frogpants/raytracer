from tools import snap
from camera import cam
from detect import on_screen
from optimization import get_image, get_rect
from msg_json import read_json, update_json
from setup import screen, img_path
import mouse_data
from editor import tile_data
from screen_data import half_width, half_height

import pygame
import random as r

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
            # blit the image (falls back to rect if image missing)
            try:
                surface = get_image(img)
                screen.blit(surface, (int(tx), int(ty)))
            except Exception:
                # fallback to debug rect if loading/blitting fails
                pygame.draw.rect(screen, (255, 255, 255), get_rect(int(tx), int(ty)))
            if (tile["collidable"]):
                package = self.tile_package(tx, ty)
                self.collision_data.append(package)
            if (tile["interactable"]):
                package = self.tile_package(tx, ty)
                self.interact_data.append(package)
    
    def editor(self):
        tx, ty = snap(mouse_data.mouse_x + cam.x, 32) - cam.x, snap(mouse_data.mouse_y + cam.y, 32) - cam.y
        img = "python-game/imgs/tile4.png"
        try:
            surface = get_image(img)
            screen.blit(surface, (int(tx), int(ty)))
        except Exception:
            pygame.draw.rect(screen, (255, 255, 255), get_rect(int(tx), int(ty)))
        if mouse_data.mouse_down:
            tile_data["x"] = tx + cam.x
            tile_data["y"] = ty + cam.y
            tile_data["type"] = r.randint(0, 3)
            self.add_tile(**tile_data)
            update_json(self.json_path, self.tile_data)

tile_controller = Tiles()
