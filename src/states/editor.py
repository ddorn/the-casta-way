from pprint import pprint

import pygame
from pygame import Vector2 as Vec
import pygame.gfxdraw

from src.camera import Camera
from src.constants import GAME_SIZE
from src.entities.decor import Rock, Beer
from src.structures import Structure, Elt
from src.window import State


class EditorState(State):
    BG_COLOR = 0x222222
    GRID_SIZE = 15
    LINE_COLOR = (100, 100, 100)

    def __init__(self, name):
        self.name = name

        try:
            struct = Structure.load(name)
            pprint(struct.elts)
            elts = {
                tuple(e.pos): Elt.name_to_class(e.type)
                for e in struct.elts
            }
        except:
            print(f"Could not load {name}. Starting new file.")
            elts = {}

        self.elts = elts
        self.elts_grid = {}

        self.brushes = [Rock, Beer]
        self.brush = 0
        self.camera = Camera()
        self.clip_to_grid = True

    def key_down(self, event):

        if event.unicode.isdigit():
            self.brush = int(event.unicode)
        elif event.key == pygame.K_LEFT:
            self.brush -= 1
        elif event.key == pygame.K_RIGHT:
            self.brush += 1
        elif event.key == pygame.K_DELETE:
            self.elts = {}
        elif event.key == pygame.K_g:
            self.clip_to_grid = not self.clip_to_grid
        elif event.key == pygame.K_s:
            self.save()

        self.brush %= len(self.brushes)

    def mouse_button(self, pos, button):
        if button == 3:
            # Erase
            if self.clip_to_grid:
                pos = (pos[0] // self.GRID_SIZE, pos[1] // self.GRID_SIZE)
                self.elts_grid.pop(pos, None)
            else:
                self.elts.pop(pos, None)
        else:
            # brush
            if self.clip_to_grid:
                pos = (pos[0] // self.GRID_SIZE, pos[1] // self.GRID_SIZE)
                self.elts_grid[pos] = self.brushes[self.brush]
            else:
                self.elts[pos] = self.brushes[self.brush]

    def draw(self, display, prop):
        display.fill(self.BG_COLOR)

        if self.clip_to_grid:
            for x in range(0, GAME_SIZE[0], self.GRID_SIZE):
                pygame.gfxdraw.vline(display, x, 0, GAME_SIZE[1], self.LINE_COLOR)

            for y in range(0, GAME_SIZE[1], self.GRID_SIZE):
                pygame.gfxdraw.hline(display, 0, GAME_SIZE[0], y, self.LINE_COLOR)

        for pos, e in self.elts.items():
            if e is not None:
                e(pos).draw(display, self.camera, prop)

        for pos, e in self.elts_grid.items():
            if e is not None:
                obj = e(self.grid_pos(pos, e))
                obj.draw(display, self.camera, prop)

        return self

    def grid_pos(self, pos, e):
        pos = Vec(pos) * self.GRID_SIZE
        if e == Beer:
            pos += (5, 5)

        return pos

    def save(self):
        min_x = min(
            min((pos[0] for pos in self.elts), default=1000),
            min((self.grid_pos(pos, e)[0] for pos, e in self.elts_grid), default=1000),
        )
        min_y = min(
            min((pos[1] for pos in self.elts), default=1000),
            min((self.grid_pos(pos, e)[1] for pos, e in self.elts_grid), default=1000),
        )

        min_pos = Vec(min_x, min_y)

        elts = [
            Elt(e.__name__, tuple(pos - min_pos))
            for pos, e in self.elts.items()
        ] + [
            Elt(e.__name__, tuple(self.grid_pos(pos, e) - min_pos))
            for pos, e in self.elts_grid.items()
        ]

        struct = Structure(self.name, elts)
        struct.save()
