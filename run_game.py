import sys

if sys.version_info < (3, 7):
    print("You need at least python 3.7")
    sys.exit(1)

try:
    import pygame
except ImportError:
    print("You need to have pygame installed")
    print("Run \033[31m pip install pygame \033[m to get it")
    sys.exit(1)

try:
    import click
except ImportError:
    print("You need to have click installed")
    print("Run \033[31m pip install click \033[m to get it")
    sys.exit(1)

try:
    import requests
except ImportError:
    print("You need to have requests installed")
    print("Run \033[31m pip install requests \033[m to get it")
    sys.exit(1)

if __name__ == "__main__":
    from src import the_casta_way

    sys.exit(the_casta_way())
