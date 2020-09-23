from src.window import State


class GameState(State):
    def draw(self, display):
        display.fill(0x222222)