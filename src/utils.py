"""
Here you can find utility functions used anywhere else in the code.
Mostly they are mathematical functions or conversion.
"""

def i(vec):
    """Convert a pygame Vector to a tuple of ints."""

    return (int(round(vec.x)), int(round(vec.y)))