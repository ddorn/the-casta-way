import pygame

from .constants import *

def the_casta_way():

    SIZE = (500, 360)

    # The display surface where we draw what will show up
    # on the screen
    display = pygame.display.set_mode(SIZE)

    # This clock object lets us fix the framerate
    clock = pygame.time.Clock()

    while True:

        # First thing to do is get the inputs
        # Otherwise the game will just not respond to the OS
        # And the OS will think it crashed.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Then we update the logic of our game
        # Which means we do nothing for now...
        ...

        # And finally we draw it to the screen
        display.fill(BG_COLOR)  # erase everything with the background color

        # And update the whole screen : in the previous step we
        # just wrote colors in the screen memory
        # but now we tell the OS to take those colors
        # and show them on your display
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    print("To run the game, you need to start 'run_game.py', not this file.")