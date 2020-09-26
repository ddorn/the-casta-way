from pygame import Vector2 as Vec

from src.animation import Sprite, Animation
from src.constants import Files, GAME_SIZE
from src.entities import Entity
from src.utils import load_cached_image


class Tree(Entity):
    SOLID = True

    def __init__(self, root_pos, layer):
        tree = load_cached_image(Files.IMAGES / "tree.png")
        size = (18, 36)
        offset = (-15, -17)
        pos = Vec(root_pos) - (9, 31)

        super().__init__(pos, size, Sprite(tree, offset), layer, wrap=True)
        self.vel = Vec( - layer * 0.2, 0)


class Rock(Entity):
    SOLID = True

    def __init__(self, pos, wrap=False):
        rock = load_cached_image(Files.IMAGES / "rock.png")
        self.wrap = wrap
        super(Rock, self).__init__(pos, rock.get_size(), Sprite(rock), wrap=wrap)


class Beer(Entity):
    SOLID = True

    def __init__(self, pos):
        size = (8, 9)
        offset = (-1, -3)
        super().__init__(pos, size, Animation.from_sheet(Files.IMAGES / "beer.png", 9, 4, offset))


class Trunk(Entity):
    SOLID = True

    def __init__(self, pos):
        trunk = Sprite(load_cached_image(Files.IMAGES / "trunk.png"))
        super().__init__(pos, (18, 18), trunk)

class Bush(Entity):
    SOLID = True
    def __init__(self, pos):
        bush = Sprite(load_cached_image(Files.IMAGES / "bush.png"))
        super().__init__(pos, (15, 15), bush)

class Fence(Entity):
    SOLID = True

    def __init__(self, pos):
        fence = Sprite(load_cached_image(Files.IMAGES / "fence.png"))
        super().__init__(pos, (15, 15), fence, wrap=True)

class Bounce(Entity):
    SOLID = True
    KNOCKBACK = 16

    def __init__(self, pos):
        bounce = Animation.from_sheet(Files.IMAGES / "bounce.png", 19, 3, (-2, -2))
        super().__init__(pos, (13, 13), bounce)

    def on_collision(self, player, dir):
        player.knock_back = -dir.normalize() * self.KNOCKBACK