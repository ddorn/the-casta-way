from pprint import pprint

import pygame
from pygame import Vector2 as Vec
import pygame.gfxdraw

from src.camera import Camera
from src.constants import GAME_SIZE, WHITE
from src.entities.decor import Rock, Beer, Trunk, Boost
from src.structures import Structure, Elt, OBJECTS
from src.utils import draw_text
from src.window import State


class EditorState(State):
    BG_COLOR = 0x222222
    GRID_SIZE = 15
    LINE_COLOR = (100, 100, 100)

    def __init__(self, name):
        self.name = name

        self.elts = {}
        self.elts_grid = {}

        try:
            struct = Structure.load(name)
            pprint(struct.elts)

            for e in struct.elts:
                on_grid, pos = self.on_grid(e.pos, e.klass)
                if on_grid:
                    self.elts_grid[pos] = e.klass
                else:
                    self.elts[pos] = e.klass
        except FileNotFoundError:
            print(f"Could not find {name}. Starting new file.")

        self.brushes = OBJECTS
        self.brush = 0
        self.camera = Camera()
        self.clip_to_grid = True

    def on_grid(self, pos, brush):
        as_grid = Vec(pos) // self.GRID_SIZE
        if pos == self.grid_pos(as_grid, brush):
            return True, tuple(as_grid)
        return False, tuple(pos)


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
        elif button == 4:
            self.brush -= 1
        elif button == 5:
            self.brush += 1
        else:
            # brush
            if self.clip_to_grid:
                pos = (pos[0] // self.GRID_SIZE, pos[1] // self.GRID_SIZE)
                self.elts_grid[pos] = self.brushes[self.brush]
            else:
                self.elts[pos] = self.brushes[self.brush]

        self.brush %= len(self.brushes)

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

        for i, o in enumerate(self.brushes):
            label = draw_text(str(i), WHITE if i != self.brush else (255, 165, 0), None, 12)
            pos = (200 + 20 * i, 270)
            o(pos).draw(display, self.camera, prop)
            display.blit(label, pos + Vec(4, 15))

        return self

    def grid_pos(self, pos, e):
        pos = Vec(pos) * self.GRID_SIZE
        if e == Beer:
            pos += (5, 5)
        elif issubclass(e, Boost):
            pos += (2, 2)

        return pos

    def save(self):
        min_x = min(
            min((pos[0] for pos in self.elts), default=1000),
            min((self.grid_pos(pos, e)[0] for pos, e in self.elts_grid.items()), default=1000),
        )
        min_y = min(
            min((pos[1] for pos in self.elts), default=1000),
            min((self.grid_pos(pos, e)[1] for pos, e in self.elts_grid.items()), default=1000),
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
