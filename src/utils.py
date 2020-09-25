"""
Here you can find utility functions used anywhere else in the code.
Mostly they are mathematical functions or conversion.
"""
from math import atan, pi


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