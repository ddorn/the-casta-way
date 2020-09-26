from math import pi
from random import randrange, uniform, random, choice

import pygame
from pygame import Rect
from pygame import Vector2 as Vec

from src.camera import Camera
from src.constants import Files, GAME_SIZE
from src.entities import Particle
from src.entities.decor import Tree, Beer, Fence
from src.entities.particles import ParticleSystem
from src.entities.player import Player
from src.states.gameover import GameOver
from src.states.pause import PauseState
from src.structures import Structure
from src.utils import load_cached_image
from src.window import State


class GameState(State):
    BG_COLOR = 0x222222
    ROAD_COLOR = 0xfecb20

    def __init__(self):
        self.huge_font = pygame.font.Font(str(Files.MAIN_FONT), 64)

        self.camera = Camera()

        self.player = Player()
        self.particles = ParticleSystem()
        self.entities = [self.particles, self.player]

        self.health_bar = load_cached_image(Files.IMAGES / "health_bar.png")

        self.structures = self.load_structures()
        self.struct_rects = []

        self.generate_trees()
        self.generate_border()

        self.paused = False

        pygame.mixer.music.load(str(Files.SOUNDS / 'soundtrack.ogg'))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    def load_structures(self):
        structures = []
        for f in Files.STRUCTURES.iterdir():
            if f.suffix == ".s":
                structures.append(Structure.load(f.stem))
        return structures

    @property
    def score(self):
        return int(self.camera.scroll + self.player.bonus)

    def generate_trees(self):
        # Generate trees
        x1 = 0
        x2 = 0
        for i in range(30):
            x1 += randrange(10, 30)
            pos = (x1, randrange(290, 330))
            layer = (pos[1] - 280) / 20 + 1
            self.entities.append(Tree(pos, layer))

            x2 += randrange(10, 30)
            pos = (x2, randrange(12, 60))
            layer = (pos[1]) / 75
            self.entities.append(Tree(pos, layer))

    def key_down(self, event):
        if event.key == pygame.K_m:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()

        if event.key == pygame.K_p:
            self.paused = True

        self.player.key_down(event)

    def logic(self):
        self.generate_terrain()
        self.road_particles()

        # Update each entity
        for entity in self.entities[:]:
            entity.logic(self)

            if not entity.alive:
                self.entities.remove(entity)

        self.camera.logic(self)
        self.physics()

        if self.paused:
            self.paused = False
            return PauseState(self)

        if not self.player.alive:
            pygame.mixer.music.fadeout(500)
            pygame.mixer.stop()
            return GameOver(self.score)
        return self

    def draw(self, display, prop):
        display.fill(0xc8d45d)

        # Draw the golden road
        display.fill(self.ROAD_COLOR, (0, 75, 400, 200))

        # Draw each entity, the ones ate the bottom of the screen first
        for entity in sorted(self.entities, key=lambda e: e.pos[1] + e.size[1]):
            entity.draw(display, self.camera, prop)

        # Draw the score
        score_surf = self.huge_font.render("{:04}".format(self.score), False, (240, 240, 240), self.BG_COLOR)
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

        for r in self.struct_rects[:]:
            if r.right < self.camera.scroll:
                self.struct_rects.remove(r)

        if random() < 0.04:
            s = choice(self.structures)
            y = randrange(75, 275 - s.height)
            rect = Rect(right, y, s.width + 20, s.height + 20)

            if not any(r.colliderect(rect) for r in self.struct_rects):
                self.struct_rects.append(rect)
                self.entities.extend(
                    s.spawn(Vec(right, y))
                )

        if random() < 0.04:
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
        for x in range(-100, GAME_SIZE[0] + 100, 16):
            self.entities.append(Fence((x, 60)))
            self.entities.append(Fence((x, 270)))