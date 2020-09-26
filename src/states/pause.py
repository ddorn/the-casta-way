import pygame

from src.utils import draw_text
from src.window import State


class PauseState(State):
    BG_COLOR = 0x222222
    TEXT_COLOR = (240, 240, 240)

    def __init__(self, inner):
        self.inner = inner
        self.resumed = False

    def logic(self):
        if self.resumed:
            return self.inner

        return self

    def key_down(self, event):
        if event.key == pygame.K_p:
            self.resumed = True

    def draw(self, display, prop):
        text = draw_text('Paused', (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = display.get_rect().center
        display.blit(text, text_rect)
