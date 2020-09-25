import pygame
from pygame import Vector2 as Vec

from src.utils import load_cached_image


class BaseSprite:
    def logic(self):
        pass

    def draw(self, display, pos):
        pass

class Sprite(BaseSprite):
    def __init__(self, surf, offset):
        self.surf = surf
        self.offset = Vec(offset)

    def draw(self, display, pos):
        display.blit(self.surf, pos + self.offset)


class Animation(BaseSprite):
    def __init__(self, sprites, frame_duration=3, offset=(0, 0)):
        self.sprites = sprites
        self.frame_duration = frame_duration
        self.offset = Vec(offset)

        self.frame_time_left = self.frame_duration
        self.sprite_index = 0

    @classmethod
    def from_sheet(cls, path, frame_width, frame_duration=3, offset=(0, 0)):
        atlas = load_cached_image(path)
        size = atlas.get_size()
        nb_frames = size[0] // frame_width

        sprites = []
        for i in range(nb_frames):
            sub = atlas.subsurface((i*frame_width, 0, frame_width, size[1]))
            sub.set_colorkey(0)
            sprites.append(sub)

        return cls(sprites, frame_duration, offset)

    def logic(self):
        """Advance to the next frame of the animation."""

        self.frame_time_left -= 1

        if self.frame_time_left == 0:
            # If we need to go to the next frame, we advance the index by one,
            # and we cycle back to the first if we are at the end of the list.
            self.sprite_index = (self.sprite_index + 1) % len(self.sprites)
            self.frame_time_left = self.frame_duration

    def draw(self, display, position):
        """Draw the sprite on the display at the given position. Takes the offset into account."""

        pos = position + self.offset
        sprite = self.sprites[self.sprite_index]
        display.blit(sprite, pos)


class SpriteCompo(BaseSprite):
    """A class to compose multiple spri"""
    def __init__(self, *sprites: BaseSprite):
        self.sprites = sprites

    def logic(self):
        for sprite in self.sprites:
            sprite.logic()

    def draw(self, display, pos):
        for sprite in self.sprites:
            sprite.draw(display, pos)
