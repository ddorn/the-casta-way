import pygame

from src.constants import WHITE, Files
from src.states import GameState
from src.utils import get_sound, draw_text
from src.window import State


class StoryState(State):
    BG_COLOR = 0x222222
    TEXT_COLOR = (240, 240, 240)
    DELAY = 45

    def __init__(self):
        self.duration = 0

        self.text = """In the good old days,
        the great Casta went through the haze
        to find the key
        and set happiness free
        
        Under his feet
        unveil a golden road
        He knew no defeat
        And were never slowed
        
        You follow his steps
        to find happiness        
        And perhaps you may
        ...
        on The Casta Way !
        """

        pygame.mixer.music.load(str(Files.SOUNDS / 'story.ogg'))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)


    def key_down(self, event):
        if event.key == pygame.K_SPACE:
            self.duration = 100000  # Put it an end

    def logic(self):
        self.duration += 1

        if self.duration > self.DELAY * (3 + len(self.text.splitlines())):  # Ten seconds
            pygame.mixer.music.fadeout(500)
            pygame.mixer.stop()
            return GameState()
        else:
            return self

    def draw(self, display, prop):
        display.fill(self.BG_COLOR)

        y = 20
        for i, line in enumerate(self.text.splitlines()[:self.duration // self.DELAY]):
            text = draw_text(line.strip(), WHITE, size=16)
            rect = text.get_rect()
            rect.centerx = 200
            rect.top = y
            display.blit(text, rect)
            y += rect.height

