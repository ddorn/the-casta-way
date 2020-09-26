from pathlib import Path
from pygame import Vector2 as Vec

FPS = 60
GAME_SIZE = (400, 300)
INF = float('inf')
WHITE = (240, 240, 240)
BACKGROUND = (34, 34, 34)

GOLD = (0xfe, 0xcb, 0x20)

DEBUG_STRUCT = True
DEBUG_HITBOX = False

class Files:
    # Directories
    ROOT = Path(__file__).parent.parent
    ASSETS = ROOT / "assets"
    SOUND = ASSETS / "sound"
    IMAGES = ASSETS / "images"
    FONTS = ASSETS / "fonts"
    STRUCTURES = ASSETS / "structures"
    DATA = ROOT / "data"

    # Files
    MAIN_FONT = FONTS / "ThaleahFat.ttf"
    NAME = DATA / "name"
    HASH = DATA / "hash"