import pygame

from src.entities.decor import Rock, Beer
from src.window import State


class EditorState(State):
    def __init__(self):
        self.elts = {}
        self.brushes = [None, Rock, Beer]
        self.brush = 1

    def key_down(self, event):

        if event.unicode.isdigit():
            self.brush = int(event.unicode)
        elif event.key == pygame.K_LEFT:
            self.brush -= 1
        elif event.key == pygame.K_RIGHT:
            self.brush += 1

        self.brush %= len(self.brushes)

    def mouse_button(self, event):
        if event.button == 0:
            # Erase
            ...
        else:
            # brush
            ...

    def logic(self):
        pass