from time import time, sleep
from typing import Type

import pygame
from pygame import Vector2 as Vec
from pygame import Rect

from .clock import Clock
from .constants import GAME_SIZE
from .utils import i


class State:

    def logic(self):
        """
        All the logic of the game happens here, ie. how to get from one frame to another.

        This function must return the next state of the app.
        """

        return self

    def draw(self, display, prop):
        """Here we draw everything on the display"""

    def key_down(self, event):
        pass



class Window:
    SIZE = Vec(GAME_SIZE)
    NAME = "The Casta Way"
    FPS = 60
    LOGIC_FPS = 30
    BORDER_COLOR = 0x000000

    def __init__(self, state: Type[State]):
        self.real_size = Vec(pygame.display.list_modes()[0])
        self.view_port: Rect = None
        self.view_port_display: pygame.Surface = None
        self.real_display: pygame.Surface = None
        self.display = pygame.Surface(self.SIZE)

        # Open the window
        self.set_display()
        # And set its name
        pygame.display.set_caption(self.NAME)

        self.running = True

        self.state = state()

        self.logic_clock = Clock(self.LOGIC_FPS)
        self.render_clock = Clock(self.FPS)

    def set_display(self, size=None):
        """Setup the display to a given size."""
        self.real_size = Vec(size or self.real_size)
        self.real_display = pygame.display.set_mode(i(self.real_size), pygame.RESIZABLE)
        self.real_display.fill(self.BORDER_COLOR)

        # We find the viewport so we have black border if the ratio do not match
        scale = min(self.real_size.x // self.SIZE.x, self.real_size.y // self.SIZE.y)
        area = self.SIZE * scale
        rect = Rect((self.real_size - area) / 2, area)

        self.view_port = rect
        self.view_port_display = self.real_display.subsurface(rect)

    def run(self):

        # Main loop. Each repetition is one frame.
        while self.running:
            self.events()

            while self.logic_clock.tick():
                self.state = self.state.logic()

            if self.render_clock.tick_all():
                # I disabled the interpolation because I don't know how to make it
                # work with the camera movement yet
                self.state.draw(self.display, 0 * self.logic_clock.tick_prop)

                # We scale the display to the viewport, which is the part of the window without the black borders.
                pygame.transform.scale(self.display, self.view_port.size, self.view_port_display)
                pygame.display.update()

            sleep(min(self.render_clock.time_left, self.logic_clock.time_left))

    def events(self):
        """Handle all events mostly by calling specialised functions"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE:
                self.set_display(event.size)
            elif event.type == pygame.KEYDOWN:
                self.state.key_down(event)

