import pygame
from Data.Code.settings import *
from Data.Code.helper import *


class StaticTile(pygame.sprite.Sprite):
    def __init__(self, group, pos, image):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect(topleft = pos)

class Water(pygame.sprite.Sprite):
    def __init__(self, group, pos, image):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect(topleft = pos)
        self.speed = 0.1
        self.collision = False

    def move(self):
        self.rect.centery -= self.speed

    def transparency(self):
        if self.collision:
            self.image.set_alpha(160)
        else: self.image.set_alpha(255)
    
    def update(self):
        self.move()
        self.transparency()
