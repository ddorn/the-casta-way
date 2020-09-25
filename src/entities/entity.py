from typing import List, Tuple

import pygame
from pygame import Vector2 as Vec
from pygame import Rect

from src.animation import BaseSprite


class Entity:
    DEFAULT_COLOR = 0xaabbdd

    def __init__(self, pos, size, sprite: BaseSprite = None, layer=0):
        self.pos = pos
        self.size = size
        self.vel = Vec()
        self.sprite = sprite or BaseSprite()
        self.alive = True
        self.layer = layer


    def draw(self, display, camera, prop):
        pos = self.pos + self.vel * prop

        screen_pos = camera.to_screen(pos, self.layer)
        self.sprite.draw(display, screen_pos)

        # One pixel with rect by default
        # pygame.draw.rect(display, self.DEFAULT_COLOR, (screen_pos, self.size), 1)

    def logic(self, game):
        self.sprite.logic()
