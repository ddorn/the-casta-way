import sys
import click

import pygame

from src.states import IntroState, GameState
from src.states.editor import EditorState
from src.window import Window



@click.command()
@click.option("--editor", "-e")
def the_casta_way(editor):
    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.init()

    if editor:
        return Window(lambda: EditorState(editor)).run()
    else:
        game = Window(IntroState)
        # inner = Window(GameState)
        return game.run()


if __name__ == "__main__":
    print("To run the inner, you need to start 'run_game.py', not this file.")