import pygame

from src.constants import Files
from src.states import GameState
from src.window import State


class IntroState(State):
    BG_COLOR = 0x222222
    TEXT_COLOR = (240, 240, 240)

    def __init__(self):
        self.duration = 120  # two seconds
        self.text = self.get_title_surf()

    def get_title_surf(self):
        font = pygame.font.Font(str(Files.MAIN_FONT), 32)
        text = font.render("The Casta Way", True, self.TEXT_COLOR, self.BG_COLOR)
        return text

    def logic(self):
        self.duration -= 1

        if self.duration <= 0:
            return GameState()
        else:
            return self

    def draw(self, display):
        display.fill(self.BG_COLOR)

        if self.duration % 20 < 14:
            # Every 20 frames we show the text for 14 frames
            # and hide it for the 6 next
            title_rect = self.text.get_rect()
            title_rect.center = display.get_rect().center
            display.blit(self.text, title_rect)