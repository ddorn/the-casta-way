import pygame

from src.constants import Files, WHITE
from src.window import State


class Leaderboard(State):
    BG_COLOR = 0x222222
    SCORE_COLOR = (0xfe, 0xcb, 0x20)

    def __init__(self, score, name='Bg Timide'):
        self.restart = False
        self.time = 0
        self.player_score = score
        self.player_name = name

    def logic(self):
        self.time += 1

        if self.restart:
            from src.states import GameState
            return GameState()
        else:
            return self

    def key_down(self, event):
        if event.key == pygame.K_r:
            self.restart = True

    def draw(self, display, prop):
        display.fill(self.BG_COLOR)

        leaderboard_title = self.get_text('Leaderboard', self.SCORE_COLOR)
        leaderboard_title_rect = leaderboard_title.get_rect()
        leaderboard_title_rect.top = 20
        leaderboard_title_rect.centerx = display.get_rect().centerx
        display.blit(leaderboard_title, leaderboard_title_rect)

        i = 0
        for i, score in enumerate(self.get_scores()):
            self.print_score(display, score, i)

        self.print_score(
            display,
            (self.player_name, self.player_score, 422),
             i + 1
        )

        if self.time % 40 > 24:
            restart_text = self.get_text('Press R to restart', WHITE, 16)
            restart_text_rect = restart_text.get_rect()
            restart_text_rect.bottom = 290
            restart_text_rect.centerx = display.get_rect().centerx
            display.blit(restart_text, restart_text_rect)

    def get_text(self, text, color=WHITE, size=32):
        font = pygame.font.Font(str(Files.MAIN_FONT), size)
        title = font.render(str(text), True, color, self.BG_COLOR)
        return title

    def print_score(self, display, info, i):
        name, score, rank = info
        list_item = self.get_text(f'{rank + 1}. {name} ({score})', size=16)
        list_item_rect = list_item.get_rect()
        list_item_rect.top = 40 + (i + 1) * 24
        list_item_rect.centerx = display.get_rect().centerx
        display.blit(list_item, list_item_rect)

    def get_scores(self):
        return [
            ('John', 17, 0),
            ('Gerard Depardieu', 17, 1),
            ('Leo', 17, 2),
            ('Felix Dorn', 17, 3),
            ('John Doez TheONE +', 17, 4),
            ('John', 14, 5),
            ('John', 14, 6),

        ]
