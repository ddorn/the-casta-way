import pygame

from src.states import IntroState
from src.window import Window



def the_casta_way():
    pygame.init()
    game = Window(IntroState())
    return game.run()


if __name__ == "__main__":
    print("To run the game, you need to start 'run_game.py', not this file.")