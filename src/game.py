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
    background.fill((150,200,255))

    # Blit to screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Create game objects
    print "Loading objects..."
    player = Player()
    platform_generator = PlatformGenerator()

    # TEST PLATFORMS -------------------
    testplatform1 = Platform()
    testplatform1.set_position(0, 400)
    testplatform2 = TimerPlatform()
    testplatform2.set_position(125, 400)
    

    # Object groups
    allsprites = pygame.sprite.Group((player, testplatform1, testplatform2))
    platforms = pygame.sprite.Group((testplatform1, testplatform2))
    colliders = pygame.sprite.Group()
    deadly = pygame.sprite.Group()
    flicker = pygame.sprite.Group()
    moving = pygame.sprite.Group()
    timer = pygame.sprite.Group()
    trampoline = pygame.sprite.Group()

    font = pygame.font.Font(None, 18)

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
                # FOR TESTING
                if event.key == K_ESCAPE:
                    main()
            elif event.type == KEYUP:
                if event.key == K_RIGHT or event.key == K_LEFT:
                    player.move_none()
                if event.key == K_SPACE:
                    player.stop_jump()

        # Generate platforms
        new_platform = platform_generator.update()
        if (new_platform):
            allsprites.add(new_platform)
            platforms.add(new_platform)

        # Group collidable platforms
        colliders.empty()
        #colliders.add(testplatform1)
        #colliders.add(testplatform2)
        for platform in platforms:
            if platform.collides():
                colliders.add(platform)


        allsprites.update()
        player.detect_collisions(colliders)

        # Test output
        text = font.render(player.to_string(), 1, ((255,0,0)))

        # Make sure player hasn't left the screen
        pos = player.get_position()
        if pos[0] < 0 or pos[1] < 0 or pos[0] > WINDOWWIDTH or pos[1] > WINDOWHEIGHT:
            # Reset the player (TEMPORARY)
            print("test")
            allsprites.remove(player)
            player = Player()
            allsprites.add(player)
            
        
        screen.blit(background, (0, 0))
        screen.blit(text, (10, 10))
        allsprites.draw(screen)
        pygame.display.flip()

if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()
