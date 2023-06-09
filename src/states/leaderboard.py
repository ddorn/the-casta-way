from _thread import start_new_thread

import pygame
from requests import get as fetch

from src.constants import Files, WHITE, BACKGROUND, GOLD
from src.states.theend import TheEndState
from src.utils import draw_text, colored_text
from src.window import State


class Leaderboard(State):
    BG_COLOR = BACKGROUND
    SCORE_COLOR = GOLD

    def __init__(self, score, name, hash):
        self.restart = False
        self.time = 0
        self.game_score = score
        self.from_the_end = False

        # Defined by set_scores
        self.scores = None
        self.score_id = None
        self.error_fetch = False
        start_new_thread(self.set_scores, (name, hash, score))


        pygame.mixer.music.load(str(Files.SOUNDS / 'leaderboard.wav'))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    def logic(self):
        self.time += 1

        if self.restart:
            from src.states import GameState
            pygame.mixer.music.fadeout(500)
            pygame.mixer.stop()
            return GameState()
        elif self.game_score > 100000 and not self.from_the_end:
            return TheEndState(self)
        else:
            return self

    def key_down(self, event):
        if event.key == pygame.K_r:
            self.restart = True

    def draw(self, display, prop):
        display.fill(self.BG_COLOR)

        leaderboard_title = draw_text('Leaderboard', self.SCORE_COLOR)
        leaderboard_title_rect = leaderboard_title.get_rect()
        leaderboard_title_rect.top = 20
        leaderboard_title_rect.centerx = display.get_rect().centerx
        display.blit(leaderboard_title, leaderboard_title_rect)

        if self.error_fetch:
            text = draw_text("Network error :(", (255, 0, 0))
            rect = text.get_rect()
            rect.center = (200, 150)
            display.blit(text, rect)
        elif self.scores is None:
            text = draw_text("loading...")
            rect = text.get_rect()
            rect.center = (200, 150)
            display.blit(text, rect)
        else:
            current_score = next(filter(lambda score: score.id == self.score_id, self.scores))

            is_top_8 = current_score.rank <= 8
            i = 0

            for i, score in enumerate(self.scores[:7 + is_top_8]):
                self.print_score(display, score, i, score.id == current_score.id)

            if not is_top_8:
                self.print_score(display, current_score, i + 1, True)

        if self.time % 40 > 24:
            restart_text = draw_text('Press R to restart', WHITE, size=16)
            restart_text_rect = restart_text.get_rect()
            restart_text_rect.bottom = 290
            restart_text_rect.centerx = display.get_rect().centerx
            display.blit(restart_text, restart_text_rect)

    def get_text(self, text, color=WHITE, size=32):
        font = pygame.font.Font(str(Files.MAIN_FONT), size)
        title = font.render(str(text), True, color, self.BG_COLOR)
        return title

    def print_score(self, display, score, i, current=False):
        list_item = colored_text(
            (score.rank, GOLD),
            (". ", WHITE),
            (score.name, (255, 30, 42) if current else WHITE),
            (" (", WHITE),
            (score.score, (255, 60, 120)),
            (")", WHITE),
            size=16
        )
        # list_item = draw_text(f'{rank + 1}. {name} ({score})', size=16)
        list_item_rect = list_item.get_rect()
        list_item_rect.top = 40 + (i + 1) * 24
        list_item_rect.centerx = display.get_rect().centerx
        display.blit(list_item, list_item_rect)

    def set_scores(self, name, hash, score):
        try:
            self.score_id = self.put_score(name, hash, score)

            scores = fetch('https://g7snanhwe2bmhhg2fozjnmhz1e9.felixdorn.fr/api/leaderboard').json()

            self.scores = [
                Score(**d, rank=rank + 1)
                for rank, d in enumerate(scores)
            ]
        except:
            self.error_fetch = True

    def put_score(self, name, hash, score):
        return fetch('https://g7snanhwe2bmhhg2fozjnmhz1e9.felixdorn.fr/api/new-score',
                     params={"name": name, 'hash': hash, 'score': score}).json()['id']


class Score:
    def __init__(self, id, name, score, rank):
        self.id = int(id)
        self.name = name
        self.score = int(score)
        self.rank = int(rank)
