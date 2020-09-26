from math import pi
from random import random, gauss, randrange

import pygame
from pygame import Vector2 as Vec

from src.animation import Animation, SpriteCompo, Sprite
from src.constants import Files
from src.entities import Entity, Particle
from src.entities.decor import Beer
# Directions
from src.utils import angle, get_sound

# Those correspond to the filenames of the animations
RIGHT = "right"
DOWN = "down"
LEFT = "left"
UP = "up"
# Actions
IDLE = "idle"
WALK = "walk"
ATTACK = "atk"


# index of Offset, width, speed
OFFSET = 0
WIDTH = 1
SPEED = 2

ANIMS = {
    (ATTACK, LEFT): [(-3, -2), 16, 1],
    (ATTACK, RIGHT): [(-2, -2), 16, 1],
    (ATTACK, UP): [(-10, -2), 23, 1],
    (ATTACK, DOWN): [(-3, -2), 23, 1],

    (WALK, LEFT): [(-3, -2), 16, 4],
    (WALK, RIGHT): [(-3, -2), 16, 4],
    (WALK, UP): [(-3, -2), 16, 4],
    (WALK, DOWN): [(-3, -2), 16, 4],

    (IDLE, LEFT): [(-3, -1), 16, 4],
    (IDLE, RIGHT): [(-3, -1), 16, 4],
    (IDLE, UP): [(-3, -1), 16, 4],
    (IDLE, DOWN): [(-3, -1), 16, 4],
}

ATTACK_LENGTH = ANIMS[ATTACK, LEFT][SPEED] * 6
ATTACK_COOL_DOWN = 3 + ATTACK_LENGTH


class Player(Entity):
    DEFAULT_COLOR = 0xff0000
    SPEED = 3  # Pixels per seconds
    SHADOW_SIZE = (14, 6)
    SOLID = True
    MASS = 1.0
    MAX_LIFE = 100
    BEER_LIFE = 10
    KNOCKBACK_RESIST = 0.6

    def __init__(self):
        super().__init__((50, 150), (10, 8))


        shadow = pygame.Surface(self.SHADOW_SIZE, pygame.SRCALPHA)
        pygame.draw.ellipse(shadow, (0, 0, 0, 100), ((0, 0), self.SHADOW_SIZE))
        shadow = Sprite(shadow, (-2, 4))

        self.animations = {
            (action, direction): SpriteCompo(
                shadow,
                Animation.from_sheet(
                    Files.IMAGES / f"{action}_{direction}.png",
                    width,
                    frame_duration=speed,
                    offset=offset + Vec(0, -8),
                )
            )
            for ((action, direction), (offset, width, speed)) in ANIMS.items()
        }

        self.direction = DOWN

        self.attack_duration = -1
        self.attack_cool_down = 0

        self.footstep_particle_delay = 0
        self.life = self.MAX_LIFE

        self.footstep_effect_duration = 0
        self.knock_back = Vec()

    def walking(self):
        """Whether the player is walking."""
        return self.vel.length_squared() > 1

    def attacking(self):
        return self.attack_duration >= 0

    def feet(self):
        """Return the position of the feet"""
        return self.pos + (5, 8)

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

        if self.attacking():
            action = ATTACK
            # Here we need to coordinate more, because if
            # The animation starts at the 3rd frame because it
            # was not reset, it looks weird
            self.animations[action, self.direction].sprite_index = 5 - self.attack_duration // ANIMS[ATTACK, LEFT][SPEED]

        self.sprite = self.animations[action, self.direction]

    def logic(self, game):
        super().logic(game)

        self.life -= 0.2
        if self.life < 0:
            self.alive = False

        self.attack(game)
        self.move(game)

        self.set_sprite()
        self.foot_particles(game)
        self.footstep_sounds()


    def move(self, game):
        inputs = pygame.key.get_pressed()

        speed_x = inputs[pygame.K_RIGHT] - inputs[pygame.K_LEFT]
        speed_y = inputs[pygame.K_DOWN] - inputs[pygame.K_UP]


        dir = Vec(speed_x, speed_y)
        if speed_x or speed_y:
            dir.scale_to_length(self.SPEED)

        self.vel = (self.vel + dir * (1 + 2*self.attacking())) / 2 + self.knock_back
        self.knock_back *= self.KNOCKBACK_RESIST

        # We clamp the position to the screen
        # if self.pos.x < inner.camera.scroll:
        #     self.pos.x = inner.camera.scroll
        #     self.vel.x = 0

    def key_down(self, event):
        if event.key == pygame.K_SPACE:
            # Attack
            if self.attack_cool_down <= 0:
                self.attack_cool_down = ATTACK_COOL_DOWN
                self.attack_duration = ATTACK_LENGTH

    def attack(self, game):
        self.attack_cool_down -= 1
        self.attack_duration -= 1

        if self.attacking():
            # Check for enemies...
            ...

    def on_collision(self, other, dir):
        ...


    def foot_particles(self, game):
        if self.walking():
            self.footstep_particle_delay -= 1

        # if self.footstep_particle_delay <= 0:
        if random() < self.vel.length_squared() / (self.SPEED ** 2 * 6):
            self.footstep_particle_delay = randrange(3, 8)

            a = gauss(angle(self.vel) + pi, 0.5)
            s = gauss(0.5, 0.1)

            game.particles.add(Particle(
                self.feet(),
                speed=s,
                angle=a,
                friction=0.05,
                size=randrange(1, 3),
                color=0x995544
            ))

    def footstep_sounds(self):
        if self.footstep_effect_duration % 9 == 0 and self.walking():
            get_sound('footstep').play()

        self.footstep_effect_duration += 1

        if not self.walking():
            self.footstep_effect_duration = 0

