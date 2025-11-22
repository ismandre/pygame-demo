# source: https://coderslegacy.com/python/python-pygame-tutorial/
import sys

import pygame
from pygame.locals import *

pygame.init()

DISPLAYSURF = pygame.display.set_mode((300,300))

# Game loop
# while True:
#     Code
#     More code
#     pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == QUIT: # Quitting the game loop
            pygame.quit()
            sys.exit()
    pygame.display.update()

# Event occurs when the user performs a specific action
# such as clicking his mouse or pressing a keyboard button

