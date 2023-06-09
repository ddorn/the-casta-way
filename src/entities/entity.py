from typing import List, Tuple

import pygame
from pygame import Vector2 as Vec
from pygame import Rect

from src.animation import BaseSprite
from src.constants import INF, GAME_SIZE, DEBUG_HITBOX


class Entity:
    DEFAULT_COLOR = 0xaabbdd
    SOLID = False
    MASS = float('inf')
    OFFSET = (0, 0)

    def __init__(self, pos, size, sprite: BaseSprite = None, layer=0, wrap=False):
        self.pos = Vec(pos)
        self.size = size
        self.vel = Vec()
        self.sprite = sprite or BaseSprite()
        self.alive = True
        self.layer = layer
        self.wrap = wrap

    def __repr__(self):
        return f"<{self.__class__.__name__}(pos={self.pos}, size={self.size})>"

    def draw(self, display, camera, prop):
        pos = self.pos + self.vel * prop

        screen_pos = camera.to_screen(pos, self.layer)
        self.sprite.draw(display, screen_pos)

        if DEBUG_HITBOX:
            # One pixel with rect by default
            pygame.draw.rect(display, self.DEFAULT_COLOR, (screen_pos, self.size), 1)

    def logic(self, game):
        self.sprite.logic()

        if self.wrap:
            screen_pos = game.camera.to_screen(self.pos, self.layer)

            # We warp it on the other side
            if screen_pos[0] < -100:
                self.pos.x += (GAME_SIZE[0] + 200)

        elif game.camera.to_screen(self.pos)[0] < -50:
            self.alive = False

    def can_collide(self, other):
        if self is other:
            return False

        # Don't do collisions between two immovable objects
        if self.MASS == other.MASS == float('inf'):
            return False

        if self.MASS != INF and other.MASS != INF:
            raise NotImplementedError

        return True

    def collide(self, other):
        return Rect(self.pos, self.size).colliderect((other.pos, other.size))

    def on_collision(self, other, dir):
        pass

    def solve_collision_x(self, other: "Entity"):
        assert self.__class__.__name__ == "Player"

        # Don't do collisions if one object is not solde
        if not self.can_collide(other):
            return

            # If we are getting out of the collision
            # prod = self.vel.x * other.vel.x
            # if prod < 0 or (prod == 0 and (self.pos.x - other.pos.x) * (self.vel.x - other.vel.x) < 0):
            #     return

        if self.collide(other):
            if other.SOLID:
                if self.vel.x > 0:
                    self.pos.x = other.pos.x - self.size[0]
                elif self.vel.x < 0:
                    self.pos.x = other.pos.x + other.size[0]

            dir = Vec(self.vel.x, 0)
            self.on_collision(other, dir)
            other.on_collision(self, dir)
            #
            # coeff1 = other.MASS / (self.MASS + other.MASS) if other.MASS != INF else 0
            # coeff2 = self.MASS / (self.MASS + other.MASS) if self.MASS != INF else 0
            #
            # self.vel.x = -self.vel.x * coeff1
            # other.vel.x = -other.vel.x * coeff2
            #


    def solve_collision_y(self, other: "Entity"):
        # Don't do collisions if one object is not solde
        if not self.can_collide(other):
            return

        if self.collide(other):
            if other.SOLID:
                if self.vel.y > 0:
                    self.pos.y = other.pos.y - self.size[1]
                elif self.vel.y < 0:
                    self.pos.y = other.pos.y + other.size[1]

            dir = Vec(0, self.vel.y)
            self.on_collision(other, dir)
            other.on_collision(self, dir)
