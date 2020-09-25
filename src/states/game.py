from random import randrange

import pygame

from src.camera import Camera
from src.constants import Files, GAME_SIZE
from src.entities.decor import Decor
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

        for i in range(8):
            pos = (randrange(-100, GAME_SIZE[0] + 100), randrange(280, 330))
            layer = (pos[1] - 280) / 20 + 1
            self.entities.append(Decor(pos, layer))

        for i in range(8):
            pos = (randrange(-100, GAME_SIZE[0] + 100), randrange(12, 75))
            layer = (pos[1]) / 75
            self.entities.append(Decor(pos, layer))

    def logic(self):
        self.score += 1

        # Update each entity
        for entity in self.entities[:]:
            entity.logic(self)

            if not entity.alive:
                self.entities.remove(entity)

        self.camera.logic(self)

        return self

    def draw(self, display, prop):
        display.fill(self.BG_COLOR)

        # Draw the golden road
        display.fill(0xfecb20, (0, 75, 400, 200))

        # Draw each entity, the ones ate the bottom of the screen first
        for entity in sorted(self.entities, key=lambda e: (e.layer, e.pos[1] + e.size[1])):
            entity.draw(display, self.camera, prop)

        # Draw the score
        score_surf = self.huge_font.render("{:04}".format(self.score), False, (240, 240, 240), self.BG_COLOR)
        rect = score_surf.get_rect()
        # rect.top = -10
        rect.centerx = 200
        display.blit(score_surf, rect)
