import pygame
from pygame import Vector2 as Vec

from src.animation import Sprite, Animation
from src.constants import Files, GAME_SIZE
from src.entities import Entity
from src.utils import load_cached_image


class Tree(Entity):
    SOLID = True

    def __init__(self, root_pos, layer):
        tree = load_cached_image(Files.IMAGES / "tree.png")
        size = (18, 36)
        offset = (-15, -17)
        pos = Vec(root_pos) - (9, 31)

        super().__init__(pos, size, Sprite(tree, offset), layer)
        self.vel = Vec( - layer * 0.2, 0)

    def logic(self, game):
        screen_pos = game.camera.to_screen(self.pos, self.layer)

        # We warp it on the other side
        if screen_pos[0] < -100:
            self.pos.x += (GAME_SIZE[0] + 200)
        elif screen_pos[0] > GAME_SIZE[0] + 100:
            self.pos.x -= GAME_SIZE[0] + 100

class Rock(Entity):
    SOLID = True

    def __init__(self, pos):
        rock = load_cached_image(Files.IMAGES / "rock.png")
        super(Rock, self).__init__(pos, rock.get_size(), Sprite(rock))

class Beer(Entity):
    SOLID = True

    def __init__(self, pos):
        size = (8, 9)
        offset = (-1, -3)
        super().__init__(pos, size, Animation.from_sheet(Files.IMAGES / "beer.png", 9, 4, offset))

