"""
Here you can find utility functions used anywhere else in the code.
Mostly they are mathematical functions or conversion.
"""
from functools import lru_cache
from math import atan, pi

import pygame

from src.constants import Files, BACKGROUND, WHITE


def i(vec):
    """Convert a pygame Vector to a tuple of ints."""

    return (int(round(vec.x)), int(round(vec.y)))


def angle(vec) -> "radians":
    x, y = vec

    if abs(x) < 1e-5:
        if y > 0:
            return pi / 2
        return 3 / 2 * pi

    a = atan(y / x)

    if x < 0:
        return a + pi
    return a


@lru_cache()
def load_cached_image(path, with_transparency=False):
    surf = pygame.image.load(str(path))
    print(f"Load {path}, {surf.get_width()}x{surf.get_height()}")

    # convert and convert_alpha give optimised versions for bliting
    if with_transparency:
        return surf.convert()
    else:
        return surf.convert_alpha()


@lru_cache()
def get_font(size, path=Files.MAIN_FONT):
    return pygame.font.Font(str(path), size)


@lru_cache(maxsize=100)
def draw_text(text, color=WHITE, bg_color=BACKGROUND, size=32, font_path=Files.MAIN_FONT):
    font = get_font(size, font_path)
    return font.render(text, False, color, bg_color)


@lru_cache(maxsize=100)
def get_sound(name, volume=1):
    sound = pygame.mixer.Sound((str(Files.SOUNDS / (name + '.wav'))))
    sound.set_volume(volume)

    return sound


def colored_text(*args, bg=BACKGROUND, size=32, font_path=Files.MAIN_FONT):
    """
    Draw a line of colored text. The args are tuples (text, color)
    that will be rendered in the given order.
    """
    font = get_font(size, font_path)

    if not args:
        return pygame.Surface((1, font.get_height()))

    surfs = [font.render(str(text), False, color, bg) for text, color in args]
    width = [s.get_width() for s in surfs]

    text = pygame.Surface((sum(width), font.get_height()))

    current_x = 0
    for s, w in zip(surfs, width):
        text.blit(s, (current_x, 0))
        current_x += w

    return text
