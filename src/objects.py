import pygame, sys, os
from pygame.locals import *
from constants import *
from utils import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('guy16.png', -1)

    def update(self):
        self.rect.topleft = (50, 50)
        
    

