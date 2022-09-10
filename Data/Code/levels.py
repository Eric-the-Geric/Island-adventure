# Imports

import pygame
import random
from Data.Code.settings import *
from Data.Code.helper import *
from Data.Code.camera import Camera
from Data.Code.level_data import *
from Data.Code.player import Player
from Data.Code.tile import *

class Test_level:
    def __init__(self):

        # Get the current surface
        self.surface = pygame.display.get_surface()

        # Initialize the sprite groups
        self.player_group = pygame.sprite.GroupSingle()
        self.collision_group = pygame.sprite.Group()
        self.water_group = pygame.sprite.Group()
        self.camera_group = Camera()
        self.power_group = pygame.sprite.Group()
        self.tree_group = pygame.sprite.Group()
        self.bridge_group = pygame.sprite.Group()
        self.sand_group = pygame.sprite.Group()

        # Getting the layout data
        self.player_layout = import_map_data(Level_test["Player"])
        self.terrain_layout = import_map_data(Level_test["Sand"])
        self.tree_layout = import_map_data(Level_test["Tree"])
        self.water_layout = import_map_data(Level_test["Water"])
        self.clouds_layout = import_map_data(Level_test["Clouds"])
        self.bridge_layout = import_map_data(Level_test["Bridge"])

        # set up the images
        self.terrain_image = import_complicated_full_sprite_sheet(Level_graphics["Sand"], tile_size, tile_size)
        self.tree_image = import_complicated_full_sprite_sheet(Level_graphics["Tree"], tile_size, tile_size)
        self.water_image = import_complicated_full_sprite_sheet(Level_graphics["Water"], tile_size, tile_size)
        self.clouds_image = import_complicated_full_sprite_sheet(Level_graphics["Clouds"], tile_size, tile_size)
        self.bridge_image = import_complicated_full_sprite_sheet(Level_graphics["Bridge"], tile_size, tile_size)

        # the powerup
        self.coconut_image = import_complicated_full_sprite_sheet(Level_graphics["Coconut"], 14, 14)


        # Set up the sprites
        self.player = self._create_player(self.player_layout)
        self._create_terrain(self.terrain_layout, "terrain", self.terrain_image)
        self._create_terrain(self.tree_layout, "tree", self.tree_image)
        self._create_terrain(self.bridge_layout, "bridge", self.bridge_image)
        self._create_terrain(self.clouds_layout, "clouds", self.clouds_image)
        self.water = self._create_terrain(self.water_layout, "water", self.water_image)

    def run(self, event_list):
        if self.player.dead:
            print("oof")
            self.player.breath = 100
            self.player.dead = False
            return True

    
        self.camera_group.custom_draw(self.player)
        self.water_group.update()
        self.player_group.update(event_list)
        self.sand_group.update()



    def _create_player(self, layout):
        for row_index, row in enumerate(layout):
                for col_index, value in enumerate(row):
                    if value != '-1':
                        if value == '0':
                            y = row_index *tile_size
                            x = col_index *tile_size
                            return Player([self.player_group, self.camera_group], (x, y), self.collision_group, self.water_group, self.tree_group, self.bridge_group, self.sand_group)
    
    
    def _create_terrain(self, layout, type, image):
            for row_index, row in enumerate(layout):
                    for col_index, value in enumerate(row):
                        y = row_index *tile_size
                        x = col_index *tile_size
                        if value != "-1":
                            if type == "terrain":
                                if value == "4":
                                    SandTile([self.collision_group, self.sand_group, self.camera_group], (x, y), image[int(value)])
                                else:
                                    StaticTile([self.collision_group, self.camera_group], (x, y), image[int(value)])
                            if type == "tree":
                                StaticTile([self.camera_group, self.tree_group], (x, y), image[int(value)])
                            if type == "water":
                                WaterTile([self.camera_group, self.water_group], (x, y), image[int(value)])
                            if type == "clouds":
                                StaticTile([self.camera_group], (x, y), image[int(value)])
                            if type == "bridge":
                                StaticTile([self.camera_group, self.bridge_group], (x, y), image[int(value)])