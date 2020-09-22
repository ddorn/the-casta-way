import sys

if sys.version_info < (3, 7):
    print("You need at least python 3.7")
    exit(1)

try:
    import pygame
except ImportError:
    print("You need to have pygame installed")
    print("Run  pip install pygame  to get it")
    quit(1)


if __name__ == "__main__":
    from src import the_casta_way

    quit(the_casta_way())