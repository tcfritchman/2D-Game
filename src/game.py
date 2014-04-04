import pygame, sys, os
from constants import *
from pygame.locals import *

def main():
    # Initialize the screen
    pygame.init()
    screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption("2D Game")
    
    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 255, 10))

    # Blit to screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Game loop
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return

        screen.blit(background, (0, 0))
        pygame.display.flip()

if __name__ == '__main__': main()



