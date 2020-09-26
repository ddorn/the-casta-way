from pathlib import Path
from pygame import Vector2 as Vec

FPS = 60
GAME_SIZE = (400, 300)
INF = float('inf')
MAX_SPEED = 15

WHITE = (240, 240, 240)
BACKGROUND = (34, 34, 34)
GOLD = (0xfe, 0xcb, 0x20)

DEBUG_STRUCT = False
DEBUG_HITBOX = False
DEBUG_STORY = False

VOLUME = {
    "boost": 1,
    "bounce": 1,
    "footstep": 0.3,
    "intro": 1,
    "pickup": 0.1,
    "soundtrack": 0.7,
    "diamond_pickup": 1,
    "lost": 1,
    "leaderboard": 1,
    "story": 1
}

class Files:
    # Directories
    ROOT = Path(__file__).parent.parent
    ASSETS = ROOT / "assets"
    SOUNDS = ASSETS / "sounds"
    IMAGES = ASSETS / "images"
    FONTS = ASSETS / "fonts"
    STRUCTURES = ASSETS / "structures"
    DATA = ROOT / "data"

    # Files
    MAIN_FONT = FONTS / "ThaleahFat.ttf"
    NAME = DATA / "name"
    HASH = DATA / "hash"