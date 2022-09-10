import pygame
from Data.Code.settings import *
from Data.Code.helper import *


class StaticTile(pygame.sprite.Sprite):
    def __init__(self, group, pos, image):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect(topleft = pos)
