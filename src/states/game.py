import pygame

from src.constants import Files
from src.entities.particles import ParticleSystem
from src.entities.player import Player
from src.window import State


class GameState(State):
    BG_COLOR = 0x222222

    def __init__(self):
        self.score = 0
        self.huge_font = pygame.font.Font(str(Files.MAIN_FONT), 64)

        self.player = Player()
        self.particles = ParticleSystem()
        self.entities = [self.particles, self.player]

    def logic(self):
        self.score += 1

        # Update each entity
        for entity in self.entities[:]:
            entity.logic(self)

            if not entity.alive:
                self.entities.remove(entity)

        return self

    def draw(self, display, prop):
        display.fill(self.BG_COLOR)

        # Draw the golden road
        display.fill(0xfecb20, (0, 75, 400, 200))

        # Draw each entity
        for entity in self.entities:
            entity.draw(display, prop)

        # Draw the score
        score_surf = self.huge_font.render("{:04}".format(self.score), False, (240, 240, 240), self.BG_COLOR)
        rect = score_surf.get_rect()
        rect.top = 20
        rect.centerx = 200
        display.blit(score_surf, rect)
