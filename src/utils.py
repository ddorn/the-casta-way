"""
Here you can find utility functions used anywhere else in the code.
Mostly they are mathematical functions or conversion.
"""
from functools import lru_cache
from math import atan, pi

import pygame


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