from src.constants import WHITE
from src.states import GameState
from src.utils import get_sound, draw_text
from src.window import State


class StoryState(State):
    BG_COLOR = 0x222222
    TEXT_COLOR = (240, 240, 240)

    def __init__(self):
        self.duration = 300  # Ten seconds

        get_sound('intro').play()

    def logic(self):
        self.duration -= 1

        if self.duration <= 0:
            return GameState()
        else:
            return self

    def draw(self, display, prop):
        display.fill(self.BG_COLOR)

        text = """The Casta Way is a long road made of gold
by Casta himself in the ancient times.
According to the legend, Casta hid the secret of happiness at the end of that road,
but there are many obstacles in the way... 

Good luck to all of us, 
and we hope that you too
will find the secret of happiness.

Casta's Disciple""".splitlines()

        for i, line in enumerate(text):
            text = draw_text(line, WHITE, size=16)
            text_rect = text.get_rect()
            text_rect.centerx = display.get_rect().centerx
            text_rect.centery = (display.get_rect().centery / 2) + i * 15
            display.blit(text, text_rect)
