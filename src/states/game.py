from math import pi
from random import randrange, gauss, uniform, random

import pygame

from src.camera import Camera
from src.constants import Files, GAME_SIZE
from src.entities import Particle
from src.entities.decor import Tree, Rock
from src.entities.particles import ParticleSystem
from src.entities.player import Player
from src.window import State


class GameState(State):
    BG_COLOR = 0x222222

    def __init__(self):
        self.score = 0
        self.huge_font = pygame.font.Font(str(Files.MAIN_FONT), 64)

        self.camera = Camera()

        self.player = Player()
        self.particles = ParticleSystem()
        self.entities = [self.particles, self.player]

        # Generate trees
        for i in range(8):
            pos = (randrange(-100, GAME_SIZE[0] + 100), randrange(280, 330))
            layer = (pos[1] - 280) / 20 + 1
            self.entities.append(Tree(pos, layer))
        for i in range(8):
            pos = (randrange(-100, GAME_SIZE[0] + 100), randrange(12, 75))
            layer = (pos[1]) / 75
            self.entities.append(Tree(pos, layer))

    def key_down(self, event):
        self.player.key_down(event)

    def logic(self):
        self.score += 1
        self.generate_terrain()
        self.road_particles()

        # Update each entity
        for entity in self.entities[:]:
            entity.logic(self)

            if not entity.alive:
                self.entities.remove(entity)

        self.camera.logic(self)
        self.physics()

        return self

    def draw(self, display, prop):
        display.fill(self.BG_COLOR)

        # Draw the golden road
        display.fill(0xfecb20, (0, 75, 400, 200))

        # Draw each entity, the ones ate the bottom of the screen first
        for entity in sorted(self.entities, key=lambda e: e.pos[1] + e.size[1]):
            entity.draw(display, self.camera, prop)

        # Draw the score
        score_surf = self.huge_font.render("{:04}".format(self.score), False, (240, 240, 240), self.BG_COLOR)
        rect = score_surf.get_rect()
        # rect.top = -10
        rect.centerx = 200
        display.blit(score_surf, rect)

    def generate_terrain(self):
        if random() < 0.1:
            self.entities.append(Rock(
                (self.camera.scroll + GAME_SIZE[0], randrange(75, 275))
            ))

    def road_particles(self):
        x = randrange(0, GAME_SIZE[0]) + self.camera.scroll
        y = randrange(75, 275)

        self.particles.add(Particle(
            pos=(x, y),
            speed=0.2,
            angle=-uniform(pi / 3, 2 * pi / 3),
            friction=0.01,
            size=2,
            color=0xffffcc,
        ))

    def physics(self):
        # To solve collisions we separate the X and Y axis,
        # This, way we know if the collision originated vertically
        # or horizontally and we can solve it appropiatly by
        # moving the object in the other direction

        # X axis
        for entity in self.entities:
            entity.pos.x += entity.vel.x

        for i, a in enumerate(self.entities):
            for b in self.entities[i+1:]:
                a.solve_collision_x(b)

        # Y axis
        for entity in self.entities:
            entity.pos.y += entity.vel.y

        for i, a in enumerate(self.entities):
            for b in self.entities[i+1:]:
                a.solve_collision_y(b)
