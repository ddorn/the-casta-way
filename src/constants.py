from pathlib import Path

FPS = 60
BG_COLOR = 0xffa500

class Files:
    ROOT = Path(__file__).parent.parent
    ASSETS = ROOT / "assets"
    SOUND = ASSETS / "sound"
    IMAGES = ASSETS / "images"
