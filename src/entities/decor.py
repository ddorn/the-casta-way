import pygame
from pygame import Vector2 as Vec

from src.animation import Sprite
from src.constants import Files, GAME_SIZE
from src.entities import Entity
from src.utils import load_cached_image


class Decor(Entity):
    def __init__(self, root_pos, layer):
        tree = load_cached_image(Files.IMAGES / "tree.png")
        size = tree.get_size()
        pos = Vec(root_pos) - (size[0] / 2, size[1])

        super().__init__(pos, size, Sprite(tree, Vec()), layer)

    def logic(self, game):
        screen_pos = game.camera.to_screen(self.pos, self.layer)

        # We warp it on the other side
        if screen_pos[0] < -100:
            self.pos.x += (GAME_SIZE[0] + 200)
        elif screen_pos[0] > GAME_SIZE[0] + 100:
            self.pos.x -= GAME_SIZE[0] + 100
