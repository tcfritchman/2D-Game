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
    platform_generator = PlatformGenerator()

    # Object groups
    allsprites = pygame.sprite.Group((player))
    colliders = pygame.sprite.Group()

    clock = pygame.time.Clock()

    # Game loop
    print "Objects loaded. Running game loop..."
    while 1:
        clock.tick(30)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    player.move_right()
                elif event.key == K_LEFT:
                    player.move_left()
                if event.key == K_SPACE:
                    player.jump()
            elif event.type == KEYUP:
                if event.key == K_RIGHT or event.key == K_LEFT:
                    player.move_none()
                if event.key == K_SPACE:
                    player.stop_jump()

	new_platform = platform_generator.update()
	if (new_platform):
	    colliders.add(new_platform)
	    

        allsprites.update()
        player.detect_collisions(colliders)

        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pygame.display.flip()

if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()
