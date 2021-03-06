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
        self.friction = AIR_FRICTION
        self.move_force = AIR_MOVE_FORCE
        self.jumping = False
        self.initial_jump = True
        self.flytime = 0
        self.xforce = 0
        self.yforce = 0
        self.xvelocity = 0
        self.yvelocity = 0
        self.xposition = 0
        self.yposition = 0
        self.bottom_collision = False

    def to_string(self):
        return 'xforce: {:8f}, yforce: {:8f}, xvelocity: {:8f}, yvelocity: {:8f}'.format(self.xforce, self.yforce, self.xvelocity, self.yvelocity)

    def update(self):
        # Determines all character physics

        if self.bottom_collision:
            self.move_force = PLATFORM_MOVE_FORCE
            self.friction = PLATFORM_FRICTION
            self.yforce = 0
            self.yvelocity = 0
        else:
            self.move_force = AIR_MOVE_FORCE
            self.friction = AIR_FRICTION
            self.yforce = GRAVITY

        # Calculate forces (factors in gravity)
        if self.movement == 'none':
            self.xforce = 0
        elif self.movement == 'right':
            self.xforce = self.move_force
        elif self.movement == 'left':
            self.xforce = -self.move_force

        # Add in platform force when on a platform
        #if self.bottom_collision:
        #    self.xforce += (PLATFORM_SPEED / self.friction) - self.xvelocity

        # Jump button is being held. Apply inital jump force then 'fly' force
        if self.jumping:
            if self.initial_jump:
                self.yforce = JUMP_FORCE
            #elif self.flytime < FLY_TIME:
            #    self.flytime += 1
            #    self.yforce += FLY_FORCE
            self.initial_jump = False
        else:
            self.initial_jump = True
            #self.flytime = 0

        # Calculate velocity (factors in friction)
        self.yvelocity = self.yvelocity + self.yforce
        self.xvelocity = self.friction * (self.xvelocity + self.xforce)

        # Bound the Y velocity
        if self.yvelocity < MIN_VELOCITY_Y:
            self.yvelocity = MIN_VELOCITY_Y
        elif self.yvelocity > MAX_VELOCITY_Y:
            self.yvelocity = MAX_VELOCITY_Y

        # Calculate new position
        self.xposition = self.xposition + self.xvelocity
        self.yposition = self.yposition + self.yvelocity

        # Update position and save last position
        self.last_rect = self.rect.copy()
        self.rect.topleft = (self.xposition, self.yposition)

    def get_position(self):
        return self.rect.topleft

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
            if T and B and L and R: # A collision has occurred
                if self.rect.y >= self.last_rect.y and self.last_rect.bottom <= collider.rect.top:
                    # A bottom collision has occured
                    self.bottom_collision = True
                    self.rect.bottom = collider.rect.top

                    # Determine what we've collided with and act accordingly
                    if collider.platform_type == "Timer":
                        collider.countdown()

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
        self.platform_type = "Platform"
        self.image = pygame.Surface([120, 25])
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.collidable = True
        self.deadly = False
        self.trampoline = False
        self.hastimer = False
    
    def update(self):
        #self.rect.x += PLATFORM_SPEED
        pass

    def set_position(self, x, y):
        self.rect.topleft = (x, y)

    def collides(self):
        if self.collidable:
            return True
        else:
            return False

class TimerPlatform(Platform):
    def __init__(self):
        Platform.__init__(self)
        self.platform_type = "Timer"

        self.visible = pygame.Surface([120, 25])
        self.visible.fill((255, 128, 0))
        self.invisible = pygame.Surface([120,25], pygame.SRCALPHA, 32)
        self.invisible.convert_alpha()

        self.image = self.visible
        #self.image = pygame.Surface([120, 25])
        #self.image.fill((255, 128, 0))
        self.timer_ticking = False
        self.timer_val = 0

    def update(self):
        if self.timer_ticking:
            self.timer_val += 1

            # Blink
            if (self.timer_val / 4) % 2 == 1:
                self.image = self.invisible
            else:
                self.image = self.visible
                
            if self.timer_val >= TIMER_FRAMES:
                self.collidable = False
                self.timer_ticking = False
        Platform.update(self)

    def countdown(self):
        if self.timer_ticking == False:
            self.timer_ticking = True

class PlatformGenerator:
    def __init__(self):
        self.framecounter = 0
        self._framemax = (PLATFORM_WIDTH + PLATFORM_GAP) / abs(PLATFORM_SPEED) + 1 + 3

    def update(self):
        if self.framecounter == self._framemax:
            # Generate a new platform
            plat = Platform()
            plat.set_position(WINDOWWIDTH + 20, WINDOWHEIGHT - 50)
            self.framecounter = 0
            self.framecounter += 1
            return plat
        else:
            self.framecounter += 1
            return False
    
    

