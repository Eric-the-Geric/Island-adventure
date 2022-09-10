import pygame
from helper import *
from settings import *
from level_data import *
from tile import *
from player import *
from camera import *
import random
from sound_effects import SoundEffects


class Test_level:
    def __init__(self):

        # Get the current surface
        self.surface = pygame.display.get_surface()

        # Initialize the sprite groups
        self.player_group = pygame.sprite.GroupSingle()
        self.collision_group = pygame.sprite.Group()
        self.semi_collision_gorup = pygame.sprite.Group()
        self.water_group = pygame.sprite.Group()
        self.camera_group = Camera()
        self.power_group = pygame.sprite.Group()

