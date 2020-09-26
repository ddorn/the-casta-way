import string

import pygame
from pygame import Vector2 as Vec

from src.constants import GOLD, GAME_SIZE, BACKGROUND
from src.states.leaderboard import Leaderboard
from src.utils import draw_text, colored_text
from src.window import State


class NameInputState(State):
    def __init__(self, score):
        # We need the score to pass it to the next State
        self.score = score
        self.name = "Diego"
        self.time = 0
        self.done = False

    def key_down(self, event):
        if event.key == pygame.K_BACKSPACE:
            self.name = self.name[:-1]
        elif event.key == pygame.K_RETURN:
            self.done = True
        else:
            l = event.unicode.lower()
            if l in string.ascii_letters + string.digits + " -_<>":
                self.name += l

    def cursor_color(self):
        if self.time % 20 < 16:
            return GOLD
        return BACKGROUND

    def logic(self):
        self.time += 1

        if self.done:
            return Leaderboard(self.score, self.name)
        return self

    def draw(self, display, prop):
        display.fill(BACKGROUND)

        inp = draw_text("Enter your name")
        name = colored_text(
            (self.name, GOLD),
            ("_", self.cursor_color())
        )

        center = Vec(GAME_SIZE) / 2

        rinp = inp.get_rect()
        rinp.midbottom = center
        rname = name.get_rect()
        rname.midtop = center

        display.blit(inp, rinp)
        display.blit(name, rname)
