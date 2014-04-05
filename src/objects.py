import pygame, sys, os, math
from pygame.locals import *
from constants import *
from utils import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('guy16.png', (0,0,0))
	self.last_rect = self.rect
        self.movement = 'none'
        self.jumping = False
        #self.frame_time = 1 / FPS
        self.xforce = 0
        self.yforce = 0
        self.xvelocity = 0
        self.yvelocity = 0
        self.xposition = 0
        self.yposition = 0
        self.bottom_collision = False

    def update(self):
        # Calculate forces (factors in gravity)
        if self.movement == 'none':
            self.xforce = 0
        elif self.movement == 'right':
            self.xforce = MOVE_FORCE
        elif self.movement == 'left':
            self.xforce = -MOVE_FORCE

        if self.bottom_collision:
            self.yforce = 0
            self.yvelocity = 0
        else:
            self.yforce = GRAVITY
        
        if self.jumping:
            self.yforce += JUMP_FORCE

        # Calculate velocity (factors in friction)
        self.xvelocity = FRICTION * (self.xvelocity + self.xforce)
        self.yvelocity = self.yvelocity + self.yforce

	if self.bottom_collision:
	    self.xvelocity = PLATFORM_SPEED + (FRICTION * (self.xvelocity + self.xforce))

        # Calculate new position
        self.xposition = self.xposition + self.xvelocity
        self.yposition = self.yposition + self.yvelocity

        # Update position and save last position
	self.last_rect = self.rect.copy()
        self.rect.topleft = (self.xposition, self.yposition)

    def force(self, amount):
        # Updates the force on self
        self.xforce += amount[0]
        self.yforce += amount[1]

    def move_right(self):
        self.movement = 'right'

    def move_left(self):
        self.movement = 'left'

    def move_none(self):
        self.movement = 'none'

    def jump(self):
        if self.bottom_collision or self.jumping:
            self.jumping = True

    def stop_jump(self):
        self.jumping = False

    def _reset_collisions(self):
        self.bottom_collision = False
        self.top_collision = False
        self.left_collision = False
        self.right_collision = False

    def detect_collisions(self, colliders):
        self._reset_collisions()
        colliderList = colliders.sprites()
        for collider in colliderList:
            T = False
            B = False
            L = False
            R = False
            # top line cross
            if self.rect.top < collider.rect.bottom:
                T = True
            # bottom line cross
            if self.rect.bottom > collider.rect.top:
                B = True
            # left line cross
            if self.rect.left < collider.rect.right:
                L = True
            # right line cross
            if self.rect.right > collider.rect.left:
                R = True
            if T and B and L and R:	# A collision has occurred
		if self.rect.y >= self.last_rect.y and self.last_rect.bottom <= collider.rect.top:
		    # A bottom collision has occured
                    self.bottom_collision = True
                    self.rect.bottom = collider.rect.top
        

class TestPlatform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([500, 25])
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Platform(pygame.sprite.Sprite):
    def __init__(self):
	pygame.sprite.Sprite.__init__(self)
	self.image = pygame.Surface([120, 25])
	self.image.fill((0, 0, 0))
	self.rect = self.image.get_rect()
    
    def update(self):
	self.rect.x += PLATFORM_SPEED

    def set_position(self, x, y):
	self.rect.topleft = (x, y)

class PlatformGenerator:
    def __init__(self):
        self.framecounter = 0
	self._framemax = (PLATFORM_WIDTH + PLATFORM_GAP) / abs(PLATFORM_SPEED) 

    def update():
	if self.framecounter == self._framemax:
	    # Generate a new platform
	    plat = Platform()
	    plat.set_position(WINDOWWIDTH + 20, WINDOWHEIGHT - 50)
	    self.framecounter = 0
	    self.framecounter += 1
	    return plat()
    	else:
	    self.framecounter += 1
	    return False
	
	

