from math import pi
from random import randrange, uniform, random, choice

import pygame
from pygame import Vector2 as Vec

from src.camera import Camera
from src.constants import Files, GAME_SIZE
from src.entities import Particle
from src.entities.decor import Tree, Rock, Beer
from src.entities.particles import ParticleSystem
from src.entities.player import Player
from src.states.gameover import GameOver
from src.structures import Structure
from src.utils import load_cached_image
from src.window import State


class GameState(State):
    BG_COLOR = 0x222222
    ROAD_COLOR = 0xfecb20

    def __init__(self):
        self.score = 0
        self.huge_font = pygame.font.Font(str(Files.MAIN_FONT), 64)

        self.camera = Camera()

        self.player = Player()
        self.particles = ParticleSystem()
        self.entities = [self.particles, self.player]

        self.health_bar = load_cached_image(Files.IMAGES / "health_bar.png")

        self.structures = self.load_structures()

        self.generate_trees()
        self.generate_border()

    def load_structures(self):
        structures = []
        for f in Files.STRUCTURES.iterdir():
            if f.suffix == ".s":
                structures.append(Structure.load(f.stem))
        return structures

    def generate_trees(self):
        # Generate trees
        for i in range(24):
            pos = (randrange(-100, GAME_SIZE[0] + 100), randrange(290, 330))

            layer = (pos[1] - 280) / 20 + 1
            self.entities.append(Tree(pos, layer))
        for i in range(24):
            pos = (randrange(-100, GAME_SIZE[0] + 100), randrange(12, 75))
            layer = (pos[1]) / 75
            self.entities.append(Tree(pos, layer))

    def key_down(self, event):
        self.player.key_down(event)

    def logic(self):
        self.score = int(self.camera.scroll)
        self.generate_terrain()
        self.road_particles()

        # Update each entity
        for entity in self.entities[:]:
            entity.logic(self)

            if not entity.alive:
                self.entities.remove(entity)

        self.camera.logic(self)
        self.physics()

        if not self.player.alive:
            return GameOver(self.score)
        return self

    def draw(self, display, prop):
        display.fill(self.BG_COLOR)

        # Draw the golden road
        display.fill(self.ROAD_COLOR, (0, 75, 400, 200))

        # Draw each entity, the ones ate the bottom of the screen first
        for entity in sorted(self.entities, key=lambda e: e.pos[1] + e.size[1]):
            entity.draw(display, self.camera, prop)

        # Draw the score
        score_surf = self.huge_font.render("{:04}".format(len(self.entities)), False, (240, 240, 240), self.BG_COLOR)
        rect = score_surf.get_rect()
        # rect.top = -10
        rect.centerx = 200
        display.blit(score_surf, rect)

        self.draw_health_bar(display)

    def draw_health_bar(self, display):
        prop = self.player.life / self.player.MAX_LIFE * 119


        # Draw the health bar
        rect = self.health_bar.get_rect()
        rect.midtop = (200, 54)

        display.fill(self.ROAD_COLOR, (rect.topleft + Vec(7, 3), (prop, 4)))
        display.blit(self.health_bar, rect)

    def generate_terrain(self):
        right = self.camera.scroll + GAME_SIZE[0]

        if random() < 0.01:
            s = choice(self.structures)
            y = randrange(75, 275 - s.height)
            self.entities.extend(
                s.spawn(Vec(right, y))
            )

        if random() < 0.01:
            self.entities.append(Beer(
                (self.camera.scroll + GAME_SIZE[0], randrange(75, 260))
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

        # We also use the fact that only the player can move
        # So we don't loop through each pair of entities

        # X axis
        for entity in self.entities:
            entity.pos.x += entity.vel.x

        for a in self.entities:
            self.player.solve_collision_x(a)

        # Y axis
        for entity in self.entities:
            entity.pos.y += entity.vel.y

        for a in self.entities:
            self.player.solve_collision_y(a)

    def generate_border(self):

        for x in range(-100, GAME_SIZE[0] + 100, 15):
            self.entities.append(Rock((x, 60), True))
            self.entities.append(Rock((x, 275), True))