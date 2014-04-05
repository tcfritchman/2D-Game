import pygame, sys, os
from pygame.locals import *
from constants import *
from utils import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('guy16.png', -1)
        self.movement = 'none'
        self.jumping = False
        #self.frame_time = 1 / FPS
        self.xforce = 0
        self.yforce = 0
        self.xvelocity = 0
        self.yvelocity = 0
        self.xposition = 0
        self.yposition = 0
        self.top_collision = False
        self.bottom_collision = False
        self.left_collision = False
        self.right_collision = False


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
        if self.left_collision:
            self.xforce = 0
            self.xvelocity = 0
        
        if self.jumping:
            self.yforce += JUMP_FORCE

        # Calculate velocity (factors in friction)
        self.xvelocity = FRICTION * (self.xvelocity + self.xforce)
        self.yvelocity = self.yvelocity + self.yforce

        # Calculate new position
        self.xposition = self.xposition + self.xvelocity
        self.yposition = self.yposition + self.yvelocity

        # Update position
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
            t = False
            b = False
            l = False
            r = False
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
            # top line cross
            if self.rect.top < collider.rect.top:
                t = True
            # bottom line cross
            if self.rect.bottom > collider.rect.bottom:
                b = True
            # left line cross
            if self.rect.left < collider.rect.left:
                l = True
            # right line cross
            if self.rect.right > collider.rect.right:
                r = True
            if T and B and L and R:
                if b:
                    self.top_collision = True
                    self.rect.top = collider.rect.bottom
                if t:
                    self.bottom_collision = True
                    self.rect.bottom = collider.rect.top
                if r and not (t or b):
                    self.left_collision = True
                    self.rect.left = collider.rect.right
                if l and not (t or b):
                    self.right_collision = True
                    self.rect.right = collider.rect.left




                




        
            
        

class TestPlatform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([500, 25])
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    

