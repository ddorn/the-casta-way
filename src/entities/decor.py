from pygame import Vector2 as Vec

from src.animation import Sprite, Animation
from src.constants import Files, WHITE, BACKGROUND
from src.entities import Entity
from src.utils import load_cached_image, get_font, get_sound


class Tree(Entity):
    SOLID = False

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
    SOLID = False
    LIFE = 5

    def __init__(self, pos):
        size = (8, 9)
        offset = (-1, -3)
        super().__init__(pos, size, Animation.from_sheet(Files.IMAGES / "beer.png", 9, 4, offset))

    def on_collision(self, player, dir):
        self.alive = False
        player.life = min(player.life + self.LIFE, player.MAX_LIFE)
        get_sound('pickup').play()


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
    KNOCKBACK = 14

    def __init__(self, pos):
        bounce = Animation.from_sheet(Files.IMAGES / "bounce.png", 19, 3, (-2, -2))
        super().__init__(pos, (13, 13), bounce)

    def on_collision(self, player, dir):
        player.knock_back = -dir.normalize() * self.KNOCKBACK
        get_sound('bounce').play()


class Boost(Entity):
    SOLID = False
    KNOCKBACK = 16
    IMAGE = "boost.png"
    DIR = (1, 0)

    def __init__(self, pos):
        boost = Sprite(load_cached_image(Files.IMAGES / self.IMAGE))
        super().__init__(pos, (13, 13), boost)

    def on_collision(self, player, dir):
        player.knock_back =  Vec(self.DIR) * self.KNOCKBACK
        get_sound("boost").play()

class BoostUp(Boost):
    DIR = (0, -1)
    IMAGE = "boost_up.png"


class BoostDown(Boost):
    DIR = (0, 1)
    IMAGE = "boost_down.png"


class Text(Entity):
    def __init__(self, pos, text):
        s = get_font(16).render(text, True, WHITE, BACKGROUND)
        s.set_alpha(100)
        super(Text, self).__init__(pos, s.get_size(), Sprite(s))


class Diamond(Entity):
    SOLID = False

    def __init__(self, pos, wrap=False):
        diamond = Animation.from_sheet(Files.IMAGES / "diamond.png", 14)
        super(Diamond, self).__init__(pos, (14, 13), diamond, wrap=wrap)

    def on_collision(self, other, dir):
        get_sound('diamond_pickup').play()
        other.bonus += 420
        self.alive = False
