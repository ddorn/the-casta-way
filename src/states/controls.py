import pygame

from src.constants import WHITE, Files
from src.states import GameState
from src.utils import get_sound, draw_text
from src.window import State


class ControlsState(State):
    BG_COLOR = 0x222222
    TEXT_COLOR = (240, 240, 240)
    DELAY = 45

    def __init__(self):
        self.duration = 0

        self.text = """use the arrows to move
        and space to dash
        
        Don't get too thirsty
        So drink enough beer !
        
        Have fun !
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

        y = 80
        for i, line in enumerate(self.text.splitlines()[:self.duration // self.DELAY]):
            text = draw_text(line.strip(), WHITE, size=16)
            rect = text.get_rect()
            rect.centerx = 200
            rect.top = y
            display.blit(text, rect)
            y += rect.height

