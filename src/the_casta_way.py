import sys

import pygame

from src.states import IntroState, GameState
from src.states.editor import EditorState
from src.window import Window



def the_casta_way():
    pygame.init()

    if "--editor" in sys.argv:
        return Window(EditorState).run()
    else:
        # game = Window(IntroState())
        game = Window(GameState)
        return game.run()


if __name__ == "__main__":
    print("To run the game, you need to start 'run_game.py', not this file.")