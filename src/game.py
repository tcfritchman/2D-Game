import pygame, sys, os
from constants import *
from utils import *
from objects import *
from pygame.locals import *

def main():
    # Initialize the screen
    print "Initializing..."
    pygame.init()
    screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption("2D Game")
    
    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((50, 180, 180))

    # Blit to screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Create game objects
    print "Loading objects..."
    player = Player()
    allsprites = pygame.sprite.Group((player))
    clock = pygame.time.Clock()

    # Game loop
    print "Objects loaded. Running game loop..."
    while 1:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == QUIT:
                return

        allsprites.update()

        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pygame.display.flip()

if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()
