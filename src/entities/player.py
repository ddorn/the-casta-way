from math import pi
from random import random, gauss, randrange

import pygame
from pygame import Vector2 as Vec

from src.animation import Animation, SpriteCompo, Sprite
from src.constants import Files
from src.entities import Entity, Particle

# Directions
from src.utils import angle

RIGHT = "right"
DOWN = "down"
LEFT = "left"
UP = "up"
# Actions
IDLE = "idle"
WALK = "walk"


class Player(Entity):
    DEFAULT_COLOR = 0xff0000
    SPEED = 2  # Pixels per seconds
    SHADOW_SIZE = (14, 6)

    def __init__(self):
        super().__init__((25, 150), (10, 16))


        shadow = pygame.Surface(self.SHADOW_SIZE, pygame.SRCALPHA)
        pygame.draw.ellipse(shadow, (0, 0, 0, 100), ((0, 0), self.SHADOW_SIZE))
        shadow = Sprite(shadow, (-2, 12))

        self.animations = {
            (action, direction): SpriteCompo(
                shadow,
                Animation.from_sheet(Files.IMAGES / f"{action}_{direction}.png", 16, 4, (-3, -2 + (action == IDLE)))
            )
            for direction in [RIGHT, DOWN, LEFT, UP]
            for action in [IDLE, WALK]
        }

        self.direction = DOWN

        self.foot_step_particle_delay = 0

    def walking(self):
        """Whether the player is walking."""
        return self.vel.length_squared() > 1

    def feet(self):
        """Return the position of the feet"""
        return self.pos + (5, 14)

    def get_direction(self, vel: Vec):
        if vel.x > 0.5:
            return RIGHT
        elif vel.x < -0.5:
            return LEFT
        elif vel.y < -0.5:
            return UP
        elif vel.y > 0.5:
            return DOWN

        return None

    def set_sprite(self):

        if self.walking():
            action = WALK
            self.direction = self.get_direction(self.vel)
        else:
            # We don't compute the direction here as we want it to be the last dir
            # we where facing when moving
            action = IDLE

        self.sprite = self.animations[action, self.direction]

    def logic(self, game):
        super().logic(game)

        inputs = pygame.key.get_pressed()

        speed_x = inputs[pygame.K_RIGHT] - inputs[pygame.K_LEFT]
        speed_y = inputs[pygame.K_DOWN] - inputs[pygame.K_UP]

        self.vel = (self.vel + Vec(speed_x, speed_y) * self.SPEED) / 2
        self.pos += self.vel

        # We clamp the position to the screen
        if self.pos.x < game.camera.scroll:
            self.pos.x = game.camera.scroll
            self.vel.x = 0

        self.set_sprite()

        if self.walking():
            self.foot_step_particle_delay -= 1
        if self.foot_step_particle_delay <= 0:
            self.foot_step_particle_delay = randrange(3, 8)
            a = gauss(angle(self.vel) + pi, 0.3)
            s = gauss(0.5, 0.1)

            game.particles.add( Particle(
                self.feet(),
                speed=s,
                angle=a,
                friction=0.05,
                size=randrange(1, 3),
                color=0x995544
            ) )



