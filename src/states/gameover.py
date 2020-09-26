import pygame
from pygame import Vector2 as Vec

from src.constants import Files, WHITE
from src.states.leaderboard import Leaderboard
from src.states.nameinput import NameInputState
from src.utils import colored_text, get_sound
from src.window import State


class GameOver(State):
    BG_COLOR = 0x222222
    GAME_OVER_COLOR = (0xe3, 0x17, 0x0a)
    SCORE_COLOR = (0xfe, 0xcb, 0x20)

    def __init__(self, score):
        self.duration = 60  # two seconds
        self.player_score = score
        self.text = self.get_title('Game Over', self.GAME_OVER_COLOR)
        self.score_label = self.get_title('Score: ')
        self.score = self.get_title(score, self.SCORE_COLOR)

        self.score_surf = colored_text(
            ("Score: ", WHITE),
            (score, self.SCORE_COLOR)
        )

        get_sound('lost').play()

    def logic(self):
        self.duration -= 1

        if self.duration <= 0:
            return NameInputState(self.player_score)
        else:
            return self

    def draw(self, display, prop):
        display.fill(self.BG_COLOR)

        # Every 20 frames we show the text for 14 frames
        # and hide it for the 6 next
        if self.duration % 20 < 14:

            drect = display.get_rect()

            title_rect = self.text.get_rect()
            title_rect.center = drect.center - Vec(0, 30)
            display.blit(self.text, title_rect)

            score_rect = self.score_surf.get_rect()
            score_rect.center = drect.center
            display.blit(self.score_surf, score_rect)

    def get_title(self, text, color=WHITE):
        font = pygame.font.Font(str(Files.MAIN_FONT), 32)
        title = font.render(str(text), True, color, self.BG_COLOR)
        return title
