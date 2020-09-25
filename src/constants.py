from pathlib import Path

FPS = 60
GAME_SIZE = (400, 300)
INF = float('inf')
WHITE = (240, 240, 240)

class Files:
    # Directories
    ROOT = Path(__file__).parent.parent
    ASSETS = ROOT / "assets"
    SOUND = ASSETS / "sound"
    IMAGES = ASSETS / "images"
    FONTS = ASSETS / "fonts"
    STRUCTURE = ASSETS / "structures"

    # Files
    MAIN_FONT = FONTS / "ThaleahFat.ttf"