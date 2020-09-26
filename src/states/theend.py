from src.constants import WHITE
from src.utils import draw_text
from src.window import State


class TheEndState(State):
    BG_COLOR = 0x222222
    TEXT_COLOR = (240, 240, 240)

    def __init__(self, leaderboard):
        self.duration = 30 * 4  # Ten seconds
        self.leaderboard = leaderboard
        pass

    def logic(self):
        self.duration -= 1

        if self.duration == 0:
            self.leaderboard.from_the_end = True
            return self.leaderboard

        return self

    def draw(self, display, prop):
        display.fill(self.BG_COLOR)

        text = draw_text('You\'re the goat.', WHITE)
        text_rect = text.get_rect()
        text_rect.center = display.get_rect().center
        display.blit(text, text_rect)
