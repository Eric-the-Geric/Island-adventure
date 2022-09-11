# Imports

import pygame
from Data.Code.settings import *
from Data.Code.helper import *
from Data.Code.camera import Camera
from Data.Code.level_data import *
from Data.Code.player import Player
from Data.Code.tile import *
import json


class BaseLevel:
    def __init__(self):

        # Get the current surface
        self.surface = pygame.display.get_surface()

        
        # Level data
        self.level_number = "Tutorial"
        self.Level_data = Level_test
        self.data = {
            "Tutorial": {
                "Best Time": 0,
                "coconuts_collected": 0,
                "max_coconuts": 3,
                "completed": "no"
            },
            "Level_One": {
                "Best Time": 0,
                "coconuts_collected": 0,
                "max_coconuts": 3,
                "completed": "no"
            },
            "Level_Two": {
                "Best Time": 0,
                "coconuts_collected": 0,
                "max_coconuts": 3,
                "completed": "no"
            },
            "Level_Three": {
                "Best Time": 0,
                "coconuts_collected": 0,
                "max_coconuts": 3,
                "completed": "no"
            },
            "Level_Four": {
                "Best Time": 0,
                "coconuts_collected": 0,
                "max_coconuts": 3,
                "completed": "no"
            },
            "Level_Five": {
                "Best Time": 0,
                "coconuts_collected": 0,
                "max_coconuts": 3,
                "completed": "no"
            }
        }

        try:
            with open('data.txt') as f:
                self.data = json.load(f)
        except:
            with open('data.txt', 'w') as f:
                json.dump(self.data, f)


        # Initialize the sprite groups
        self.player_group = pygame.sprite.GroupSingle()
        self.collision_group = pygame.sprite.Group()
        self.water_group = pygame.sprite.Group()
        self.camera_group = Camera()
        self.power_group = pygame.sprite.Group()
        self.tree_group = pygame.sprite.Group()
        self.bridge_group = pygame.sprite.Group()
        self.sand_group = pygame.sprite.Group()
        self.coconut_group = pygame.sprite.Group()
        self.animated_group = pygame.sprite.Group()

        # Getting the layout data
        self.player_layout = import_map_data(self.Level_data["Player"])
        self.terrain_layout = import_map_data(self.Level_data["Sand"])
        self.background_layout = import_map_data(self.Level_data["Background"])
        self.tree_layout = import_map_data(self.Level_data["Tree"])
        self.water_layout = import_map_data(self.Level_data["Water"])
        self.clouds_layout = import_map_data(self.Level_data["Clouds"])
        self.bridge_layout = import_map_data(self.Level_data["Bridge"])
        self.coconut_layout = import_map_data(self.Level_data["Coconut"])
        

        # set up the images
        self.terrain_image = import_complicated_full_sprite_sheet(Level_graphics["Sand"], tile_size, tile_size)
        self.tree_image = import_complicated_full_sprite_sheet(Level_graphics["Tree"], tile_size, tile_size)
        self.water_image = import_complicated_full_sprite_sheet(Level_graphics["Water"], tile_size, tile_size)
        self.clouds_image = import_complicated_full_sprite_sheet(Level_graphics["Clouds"], tile_size, tile_size)
        self.bridge_image = import_complicated_full_sprite_sheet(Level_graphics["Bridge"], tile_size, tile_size)
        self.background_image = import_complicated_full_sprite_sheet(Level_graphics["Background"], tile_size, tile_size)
        
        # collectables
        self.coconut_image = import_complicated_full_sprite_sheet(Level_graphics["Coconut"], 14, 14)


        # Set up the sprites
        self._create_terrain(self.background_layout, "background", self.background_image)
        self.player = self._create_player(self.player_layout)
        
        self._create_terrain(self.terrain_layout, "terrain", self.terrain_image)
        self._create_terrain(self.tree_layout, "tree", self.tree_image)
        self._create_terrain(self.bridge_layout, "bridge", self.bridge_image)
        self._create_terrain(self.clouds_layout, "clouds", self.clouds_image)
        self._create_terrain(self.coconut_layout, "coconut", self.coconut_image)
        self._create_terrain(self.water_layout, "water", self.water_image)
        

        # Level won?
        self.won = False

    def run(self, event_list, music):
        if self.player.dead:
            music.play_song("dead")
            return True

        if self.player.won:
            
            self.data[self.level_number]["completed"] = "yes"
            if self.player.collected > self.data[self.level_number]["coconuts_collected"]:
                self.data[self.level_number]["coconuts_collected"] = self.player.collected
            if self.player.speedrunner/1000 > 1 and self.player.speedrunner/1000 < self.data[self.level_number]["Best Time"] or self.data[self.level_number]["Best Time"]==0:
                self.data[self.level_number]["Best Time"] = self.player.speedrunner/1000

            with open('data.txt', 'w') as f:
                json.dump(self.data, f)
            self.won = True
        
        self.camera_group.custom_draw(self.player)
        self.animated_group.update()
        self.water_group.update()
        
        self.sand_group.update()
        self.player_group.update(event_list, music)
        



    def _create_player(self, layout):
        for row_index, row in enumerate(layout):
                for col_index, value in enumerate(row):
                    if value != '-1':
                        if value == '0':
                            y = row_index *tile_size
                            x = col_index *tile_size
                            return Player([self.player_group, self.camera_group], (x, y), self.collision_group, self.water_group, self.tree_group, self.bridge_group, self.sand_group, self.coconut_group)
    
    
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
                                WaterTile([self.camera_group, self.water_group], (x, y), image[int(value)], 0.0001)
                            if type == "clouds":
                                StaticTile([self.camera_group], (x, y), image[int(value)])
                            if type == "bridge":
                                StaticTile([self.camera_group, self.bridge_group], (x, y), image[int(value)])
                            if type == "coconut":
                                StaticTile([self.camera_group, self.coconut_group], (x+32, y+64-14), image[int(value)])
                            if type == "background":
                                AnimatedTile([self.camera_group, self.animated_group], (x, y), image)
                            
class Main_menu:
    def __init__(self):
        self.surface = pygame.display.get_surface()
        # level data
        self.Level_data = Main_menu_data
        
        # layout
        self.layout = import_map_data(self.Level_data["buttons"])
        
        # groups
        self.Tutorial = pygame.sprite.GroupSingle()
        self.Level_selection = pygame.sprite.GroupSingle()
        self.key_bindings = pygame.sprite.GroupSingle()
        self.fluffy = pygame.sprite.GroupSingle()
        self.quit = pygame.sprite.GroupSingle()


        # images
        self.image = import_complicated_full_sprite_sheet(Menu_graphics["menu"], 640, 128)

        self._create_terrain(self.layout)

    def run(self):
        self.Tutorial.draw(self.surface)
        self.Tutorial.update()
        
        self.Level_selection.draw(self.surface)
        self.Level_selection.update()
        
        self.key_bindings.draw(self.surface)
        self.key_bindings.update()
        
        self.fluffy.draw(self.surface)
        self.fluffy.update()
        
        self.quit.draw(self.surface)
        self.quit.update()
        

    def _create_terrain(self, layout):
        for row_index, row in enumerate(layout):
                for col_index, value in enumerate(row):
                    y = row_index *128
                    x = col_index *640
                    if value != "-1":
                        if value == "0":
                            MenuTile(self.Tutorial, (x,y), self.image[int(value)])
                        if value == "1":
                            MenuTile(self.Level_selection, (x,y), self.image[int(value)])
                        if value == "2":
                            MenuTile(self.key_bindings, (x,y), self.image[int(value)])
                        if value == "3":
                            MenuTile(self.fluffy, (x,y), self.image[int(value)])
                        if value == "4":
                            MenuTile(self.quit, (x,y), self.image[int(value)])

class Level_selector:
    def __init__(self):
        self.font = pygame.font.Font(None, 20)
        self.surface = pygame.display.get_surface()
        # level data
        self.Level_data = Level_selector_data
        
        # layout
        self.layout = import_map_data(self.Level_data["buttons"])
        
        # groups
        self.one = pygame.sprite.GroupSingle()
        self.two = pygame.sprite.GroupSingle()
        self.three = pygame.sprite.GroupSingle()
        self.four = pygame.sprite.GroupSingle()
        self.five = pygame.sprite.GroupSingle()
        self.data = {
            "Tutorial": {
                "Best Time": 0,
                "coconuts_collected": 0,
                "max_coconuts": 3,
                "completed": "no"
            },
            "Level_One": {
                "Best Time": 0,
                "coconuts_collected": 0,
                "max_coconuts": 3,
                "completed": "no"
            },
            "Level_Two": {
                "Best Time": 0,
                "coconuts_collected": 0,
                "max_coconuts": 3,
                "completed": "no"
            },
            "Level_Three": {
                "Best Time": 0,
                "coconuts_collected": 0,
                "max_coconuts": 3,
                "completed": "no"
            },
            "Level_Four": {
                "Best Time": 0,
                "coconuts_collected": 0,
                "max_coconuts": 3,
                "completed": "no"
            },
            "Level_Five": {
                "Best Time": 0,
                "coconuts_collected": 0,
                "max_coconuts": 3,
                "completed": "no"
            }
        }

        try:
            with open('data.txt') as f:
                self.data = json.load(f)
        except:
            with open('data.txt', 'w') as f:
                json.dump(self.data, f)

        # images
        self.image = import_complicated_full_sprite_sheet(Level_selector_graphics["level"], tile_size, tile_size)

        self._create_terrain(self.layout)
        self.level_to_display = "Tutorial"

    def run(self, events):
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.level_to_display = "Tutorial"
                    if event.key == pygame.K_2:
                        self.level_to_display = "Level_One"
                    if event.key == pygame.K_3:
                        self.level_to_display = "Level_Two"
                    if event.key == pygame.K_4:
                        self.level_to_display = "Level_Three"
                    if event.key == pygame.K_5:
                        self.level_to_display = "Level_Four"
                    if event.key == pygame.K_6:
                        self.level_to_display = "Level_Five"
            self.one.draw(self.surface)
            self.one.update()
            text = self.font.render(self.level_to_display + " : " + str(self.data[self.level_to_display]), True, ("black"))
            textRect = text.get_rect()
            textRect.center = (320, 320)
            self.surface.blit(text, textRect)
                
            self.two.draw(self.surface)
            self.two.update()
            if self.two.sprite.clicked:
                pass
            self.three.draw(self.surface)
            self.three.update()
            if self.three.sprite.clicked:
                pass
            self.four.draw(self.surface)
            self.four.update()
            if self.four.sprite.clicked:
                pass
            self.five.draw(self.surface)
            self.five.update()
            if self.five.sprite.clicked:
                pass



    def _create_terrain(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, value in enumerate(row):
                y = row_index *(2*tile_size)
                x = col_index *(2*tile_size)
                if value != "-1":
                    if value == "0":
                        LevelTile(self.one, (x,y), self.image[int(value)])
                    if value == "1":
                        LevelTile(self.two, (x,y), self.image[int(value)])
                    if value == "2":
                        LevelTile(self.three, (x,y), self.image[int(value)])
                    if value == "3":
                        LevelTile(self.four, (x,y), self.image[int(value)])
                    if value == "4":
                        LevelTile(self.five, (x,y), self.image[int(value)])

class LevelOne:
    def __init__(self):
    
        # Get the current surface
        self.surface = pygame.display.get_surface()

        
        # Level data
        self.level_number = "Level_One"
        self.Level_data = Level_1
        self.data = {
            "Tutorial": {
                "Best Time": 0,
                "coconuts_collected": 0,
                "max_coconuts": 3,
                "completed": "no"
            },
            "Level_One": {
                "Best Time": 0,
                "coconuts_collected": 0,
                "max_coconuts": 3,
                "completed": "no"
            },
            "Level_Two": {
                "Best Time": 0,
                "coconuts_collected": 0,
                "max_coconuts": 3,
                "completed": "no"
            },
            "Level_Three": {
                "Best Time": 0,
                "coconuts_collected": 0,
                "max_coconuts": 3,
                "completed": "no"
            },
            "Level_Four": {
                "Best Time": 0,
                "coconuts_collected": 0,
                "max_coconuts": 3,
                "completed": "no"
            },
            "Level_Five": {
                "Best Time": 0,
                "coconuts_collected": 0,
                "max_coconuts": 3,
                "completed": "no"
            }
        }

        try:
            with open('data.txt') as f:
                self.data = json.load(f)
        except:
            with open('data.txt', 'w') as f:
                json.dump(self.data, f)


        # Initialize the sprite groups
        self.player_group = pygame.sprite.GroupSingle()
        self.collision_group = pygame.sprite.Group()
        self.water_group = pygame.sprite.Group()
        self.camera_group = Camera()
        self.power_group = pygame.sprite.Group()
        self.tree_group = pygame.sprite.Group()
        self.bridge_group = pygame.sprite.Group()
        self.sand_group = pygame.sprite.Group()
        self.coconut_group = pygame.sprite.Group()
        self.animated_group = pygame.sprite.Group()

        # Getting the layout data
        self.player_layout = import_map_data(self.Level_data["Player"])
        self.terrain_layout = import_map_data(self.Level_data["Sand"])
        self.tree_layout = import_map_data(self.Level_data["Tree"])
        self.water_layout = import_map_data(self.Level_data["Water"])
        self.clouds_layout = import_map_data(self.Level_data["Clouds"])
        self.bridge_layout = import_map_data(self.Level_data["Bridge"])
        self.coconut_layout = import_map_data(self.Level_data["Coconut"])        
        self.background_layout = import_map_data(self.Level_data["Background"])        


        # set up the images
        self.terrain_image = import_complicated_full_sprite_sheet(Level_graphics["Sand"], tile_size, tile_size)
        self.tree_image = import_complicated_full_sprite_sheet(Level_graphics["Tree"], tile_size, tile_size)
        self.water_image = import_complicated_full_sprite_sheet(Level_graphics["Water"], tile_size, tile_size)
        self.clouds_image = import_complicated_full_sprite_sheet(Level_graphics["Clouds"], tile_size, tile_size)
        self.bridge_image = import_complicated_full_sprite_sheet(Level_graphics["Bridge"], tile_size, tile_size)
        self.background_image = import_complicated_full_sprite_sheet(Level_graphics["Background"], tile_size, tile_size)
        
        # collectables
        self.coconut_image = import_complicated_full_sprite_sheet(Level_graphics["Coconut"], 14, 14)


        # Set up the sprites
        self._create_terrain(self.background_layout, "background", self.background_image)
        self.player = self._create_player(self.player_layout)
        self._create_terrain(self.terrain_layout, "terrain", self.terrain_image)
        self._create_terrain(self.tree_layout, "tree", self.tree_image)
        self._create_terrain(self.bridge_layout, "bridge", self.bridge_image)
        self._create_terrain(self.clouds_layout, "clouds", self.clouds_image)
        self._create_terrain(self.coconut_layout, "coconut", self.coconut_image)
        self._create_terrain(self.water_layout, "water", self.water_image)
        

        # Level won?
        self.won = False

    def run(self, event_list, music):
        if self.player.dead:
            music.play_song("dead")
            return True

        if self.player.won:
            music.stop_song()
            music.play_song("swon")
            
            self.data[self.level_number]["completed"] = "yes"
            if self.player.collected > self.data[self.level_number]["coconuts_collected"]:
                self.data[self.level_number]["coconuts_collected"] = self.player.collected
            if (self.player.speedrunner/1000 > 1 and self.player.speedrunner/1000 < self.data[self.level_number]["Best Time"]) or self.data[self.level_number]["Best Time"] <2:
                self.data[self.level_number]["Best Time"] = self.player.speedrunner/1000

            with open('data.txt', 'w') as f:
                json.dump(self.data, f)
            self.won = True
        self.animated_group.update()
        self.camera_group.custom_draw(self.player)
        self.water_group.update()
        self.player_group.update(event_list, music)
        self.sand_group.update()

    def _create_player(self, layout):
        for row_index, row in enumerate(layout):
                for col_index, value in enumerate(row):
                    if value != '-1':
                        if value == '0':
                            y = row_index *tile_size
                            x = col_index *tile_size
                            return Player([self.player_group, self.camera_group], (x, y), self.collision_group, self.water_group, self.tree_group, self.bridge_group, self.sand_group, self.coconut_group)
    
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
                                WaterTile([self.camera_group, self.water_group], (x, y), image[int(value)], 0.3)
                            if type == "clouds":
                                StaticTile([self.camera_group], (x, y), image[int(value)])
                            if type == "bridge":
                                StaticTile([self.camera_group, self.bridge_group], (x, y), image[int(value)])
                            if type == "coconut":
                                StaticTile([self.camera_group, self.coconut_group], (x+32, y+64-14), image[int(value)])
                            if type == "background":
                                AnimatedTile([self.camera_group, self.animated_group], (x, y), image)
      
class LevelTwo:
    def __init__(self):
        
        # Get the current surface
        self.surface = pygame.display.get_surface()

        
        # Level data
        self.level_number = "Level_Two"
        self.Level_data = Level_2
        self.data = {
            "Tutorial": {
                "Best Time": 0,
                "coconuts_collected": 0,
                "max_coconuts": 3,
                "completed": "no"
            },
            "Level_One": {
                "Best Time": 0,
                "coconuts_collected": 0,
                "max_coconuts": 3,
                "completed": "no"
            },
            "Level_Two": {
                "Best Time": 0,
                "coconuts_collected": 0,
                "max_coconuts": 3,
                "completed": "no"
            },
            "Level_Three": {
                "Best Time": 0,
                "coconuts_collected": 0,
                "max_coconuts": 3,
                "completed": "no"
            },
            "Level_Four": {
                "Best Time": 0,
                "coconuts_collected": 0,
                "max_coconuts": 3,
                "completed": "no"
            },
            "Level_Five": {
                "Best Time": 0,
                "coconuts_collected": 0,
                "max_coconuts": 3,
                "completed": "no"
            }
        }
        try:
            with open('data.txt') as f:
                self.data = json.load(f)
        except:
            with open('data.txt', 'w') as f:
                json.dump(self.data, f)


        # Initialize the sprite groups
        self.player_group = pygame.sprite.GroupSingle()
        self.collision_group = pygame.sprite.Group()
        self.water_group = pygame.sprite.Group()
        self.camera_group = Camera()
        self.power_group = pygame.sprite.Group()
        self.tree_group = pygame.sprite.Group()
        self.bridge_group = pygame.sprite.Group()
        self.sand_group = pygame.sprite.Group()
        self.coconut_group = pygame.sprite.Group()
        self.animated_group = pygame.sprite.Group()

        # Getting the layout data
        self.player_layout = import_map_data(self.Level_data["Player"])
        self.terrain_layout = import_map_data(self.Level_data["Sand"])
        self.tree_layout = import_map_data(self.Level_data["Tree"])
        self.water_layout = import_map_data(self.Level_data["Water"])
        self.clouds_layout = import_map_data(self.Level_data["Clouds"])
        self.bridge_layout = import_map_data(self.Level_data["Bridge"])
        self.coconut_layout = import_map_data(self.Level_data["Coconut"])
        self.background_layout = import_map_data(self.Level_data["Background"])

        # set up the images
        self.terrain_image = import_complicated_full_sprite_sheet(Level_graphics["Sand"], tile_size, tile_size)
        self.tree_image = import_complicated_full_sprite_sheet(Level_graphics["Tree"], tile_size, tile_size)
        self.water_image = import_complicated_full_sprite_sheet(Level_graphics["Water"], tile_size, tile_size)
        self.clouds_image = import_complicated_full_sprite_sheet(Level_graphics["Clouds"], tile_size, tile_size)
        self.bridge_image = import_complicated_full_sprite_sheet(Level_graphics["Bridge"], tile_size, tile_size)
        self.background_image = import_complicated_full_sprite_sheet(Level_graphics["Background"], tile_size, tile_size)
        
        # collectables
        self.coconut_image = import_complicated_full_sprite_sheet(Level_graphics["Coconut"], 14, 14)


        # Set up the sprites
        self._create_terrain(self.background_layout, "background", self.background_image)
        self.player = self._create_player(self.player_layout)
        self._create_terrain(self.terrain_layout, "terrain", self.terrain_image)
        self._create_terrain(self.tree_layout, "tree", self.tree_image)
        self._create_terrain(self.bridge_layout, "bridge", self.bridge_image)
        self._create_terrain(self.clouds_layout, "clouds", self.clouds_image)
        self._create_terrain(self.coconut_layout, "coconut", self.coconut_image)
        self._create_terrain(self.water_layout, "water", self.water_image)
        

        # Level won?
        self.won = False

    def run(self, event_list, music):
        if self.player.dead:
            music.play_song("dead")
            return True

        if self.player.won:
            music.stop_song()
            music.play_song("swon")
            
            self.data[self.level_number]["completed"] = "yes"
            if self.player.collected > self.data[self.level_number]["coconuts_collected"]:
                self.data[self.level_number]["coconuts_collected"] = self.player.collected
            if self.player.speedrunner/1000 > 1 and self.player.speedrunner/1000 < self.data[self.level_number]["Best Time"] or self.data[self.level_number]["Best Time"]==0:
                self.data[self.level_number]["Best Time"] = self.player.speedrunner/1000

            with open('data.txt', 'w') as f:
                json.dump(self.data, f)
            self.won = True
    
        self.camera_group.custom_draw(self.player)
        self.water_group.update()
        self.player_group.update(event_list, music)
        self.animated_group.update()
        self.sand_group.update()

    def _create_player(self, layout):
        for row_index, row in enumerate(layout):
                for col_index, value in enumerate(row):
                    if value != '-1':
                        if value == '0':
                            y = row_index *tile_size
                            x = col_index *tile_size
                            return Player([self.player_group, self.camera_group], (x, y), self.collision_group, self.water_group, self.tree_group, self.bridge_group, self.sand_group, self.coconut_group)
    
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
                                WaterTile([self.camera_group, self.water_group], (x, y), image[int(value)], 1)
                            if type == "clouds":
                                StaticTile([self.camera_group], (x, y), image[int(value)])
                            if type == "bridge":
                                StaticTile([self.camera_group, self.bridge_group], (x, y), image[int(value)])
                            if type == "coconut":
                                StaticTile([self.camera_group, self.coconut_group], (x+32, y+64-14), image[int(value)])
                            if type == "background":
                                AnimatedTile([self.camera_group, self.animated_group], (x, y), image)
   
class LevelThree:
    def __init__(self):
        
        # Get the current surface
        self.surface = pygame.display.get_surface()

        
        # Level data
        self.level_number = "Level_Three"
        self.Level_data = Level_3
        self.data = {
            "Tutorial": {
                "Best Time": 0,
                "coconuts_collected": 0,
                "max_coconuts": 3,
                "completed": "no"
            },
            "Level_One": {
                "Best Time": 0,
                "coconuts_collected": 0,
                "max_coconuts": 3,
                "completed": "no"
            },
            "Level_Two": {
                "Best Time": 0,
                "coconuts_collected": 0,
                "max_coconuts": 3,
                "completed": "no"
            },
            "Level_Three": {
                "Best Time": 0,
                "coconuts_collected": 0,
                "max_coconuts": 3,
                "completed": "no"
            },
            "Level_Four": {
                "Best Time": 0,
                "coconuts_collected": 0,
                "max_coconuts": 3,
                "completed": "no"
            },
            "Level_Five": {
                "Best Time": 0,
                "coconuts_collected": 0,
                "max_coconuts": 3,
                "completed": "no"
            }
        }
        try:
            with open('data.txt') as f:
                self.data = json.load(f)
        except:
            with open('data.txt', 'w') as f:
                json.dump(self.data, f)


        # Initialize the sprite groups
        self.player_group = pygame.sprite.GroupSingle()
        self.collision_group = pygame.sprite.Group()
        self.water_group = pygame.sprite.Group()
        self.camera_group = Camera()
        self.power_group = pygame.sprite.Group()
        self.tree_group = pygame.sprite.Group()
        self.bridge_group = pygame.sprite.Group()
        self.sand_group = pygame.sprite.Group()
        self.coconut_group = pygame.sprite.Group()
        self.animated_group = pygame.sprite.Group()

        # Getting the layout data
        self.player_layout = import_map_data(self.Level_data["Player"])
        self.terrain_layout = import_map_data(self.Level_data["Sand"])
        self.tree_layout = import_map_data(self.Level_data["Tree"])
        self.water_layout = import_map_data(self.Level_data["Water"])
        self.clouds_layout = import_map_data(self.Level_data["Clouds"])
        self.bridge_layout = import_map_data(self.Level_data["Bridge"])
        self.coconut_layout = import_map_data(self.Level_data["Coconut"])
        self.background_layout = import_map_data(self.Level_data["Background"])

        # set up the images
        self.terrain_image = import_complicated_full_sprite_sheet(Level_graphics["Sand"], tile_size, tile_size)
        self.tree_image = import_complicated_full_sprite_sheet(Level_graphics["Tree"], tile_size, tile_size)
        self.water_image = import_complicated_full_sprite_sheet(Level_graphics["Water"], tile_size, tile_size)
        self.clouds_image = import_complicated_full_sprite_sheet(Level_graphics["Clouds"], tile_size, tile_size)
        self.bridge_image = import_complicated_full_sprite_sheet(Level_graphics["Bridge"], tile_size, tile_size)
        # collectables
        self.coconut_image = import_complicated_full_sprite_sheet(Level_graphics["Coconut"], 14, 14)
        self.background_image = import_complicated_full_sprite_sheet(Level_graphics["Background"], tile_size, tile_size)

        # Set up the sprites
        self._create_terrain(self.background_layout, "background", self.background_image)
        self.player = self._create_player(self.player_layout)
        self._create_terrain(self.terrain_layout, "terrain", self.terrain_image)
        self._create_terrain(self.tree_layout, "tree", self.tree_image)
        self._create_terrain(self.bridge_layout, "bridge", self.bridge_image)
        self._create_terrain(self.clouds_layout, "clouds", self.clouds_image)
        self._create_terrain(self.coconut_layout, "coconut", self.coconut_image)
        self._create_terrain(self.water_layout, "water", self.water_image)
        

        # Level won?
        self.won = False

    def run(self, event_list, music):
        if self.player.dead:
            music.play_song("dead")
            return True

        if self.player.won:
            music.stop_song()
            music.play_song("swon")
            
            self.data[self.level_number]["completed"] = "yes"
            if self.player.collected > self.data[self.level_number]["coconuts_collected"]:
                self.data[self.level_number]["coconuts_collected"] = self.player.collected
            if self.player.speedrunner/1000 > 1 and self.player.speedrunner/1000 < self.data[self.level_number]["Best Time"] or self.data[self.level_number]["Best Time"]==0:
                self.data[self.level_number]["Best Time"] = self.player.speedrunner/1000

            with open('data.txt', 'w') as f:
                json.dump(self.data, f)
            self.won = True
    
        self.camera_group.custom_draw(self.player)
        self.water_group.update()
        self.player_group.update(event_list, music)
        self.animated_group.update()
        self.sand_group.update()

    def _create_player(self, layout):
        for row_index, row in enumerate(layout):
                for col_index, value in enumerate(row):
                    if value != '-1':
                        if value == '0':
                            y = row_index *tile_size
                            x = col_index *tile_size
                            return Player([self.player_group, self.camera_group], (x, y), self.collision_group, self.water_group, self.tree_group, self.bridge_group, self.sand_group, self.coconut_group)
    
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
                                WaterTile([self.camera_group, self.water_group], (x, y), image[int(value)], 1.1)
                            if type == "clouds":
                                StaticTile([self.camera_group], (x, y), image[int(value)])
                            if type == "bridge":
                                StaticTile([self.camera_group, self.bridge_group], (x, y), image[int(value)])
                            if type == "coconut":
                                StaticTile([self.camera_group, self.coconut_group], (x+32, y+64-14), image[int(value)])
                            if type == "background":
                                AnimatedTile([self.camera_group, self.animated_group], (x, y), image)
 
class LevelFour:
    def __init__(self):
        
        # Get the current surface
        self.surface = pygame.display.get_surface()

        
        # Level data
        self.level_number = "Level_Four"
        self.Level_data = Level_4
        self.data = {
            "Tutorial": {
                "Best Time": 0,
                "coconuts_collected": 0,
                "max_coconuts": 3,
                "completed": "no"
            },
            "Level_One": {
                "Best Time": 0,
                "coconuts_collected": 0,
                "max_coconuts": 3,
                "completed": "no"
            },
            "Level_Two": {
                "Best Time": 0,
                "coconuts_collected": 0,
                "max_coconuts": 3,
                "completed": "no"
            },
            "Level_Three": {
                "Best Time": 0,
                "coconuts_collected": 0,
                "max_coconuts": 3,
                "completed": "no"
            },
            "Level_Four": {
                "Best Time": 0,
                "coconuts_collected": 0,
                "max_coconuts": 3,
                "completed": "no"
            },
            "Level_Five": {
                "Best Time": 0,
                "coconuts_collected": 0,
                "max_coconuts": 3,
                "completed": "no"
            }
        }
        try:
            with open('data.txt') as f:
                self.data = json.load(f)
        except:
            with open('data.txt', 'w') as f:
                json.dump(self.data, f)


        # Initialize the sprite groups
        self.player_group = pygame.sprite.GroupSingle()
        self.collision_group = pygame.sprite.Group()
        self.water_group = pygame.sprite.Group()
        self.camera_group = Camera()
        self.power_group = pygame.sprite.Group()
        self.tree_group = pygame.sprite.Group()
        self.bridge_group = pygame.sprite.Group()
        self.sand_group = pygame.sprite.Group()
        self.coconut_group = pygame.sprite.Group()
        self.animated_group = pygame.sprite.Group()

        # Getting the layout data
        self.player_layout = import_map_data(self.Level_data["Player"])
        self.terrain_layout = import_map_data(self.Level_data["Sand"])
        self.tree_layout = import_map_data(self.Level_data["Tree"])
        self.water_layout = import_map_data(self.Level_data["Water"])
        self.clouds_layout = import_map_data(self.Level_data["Clouds"])
        self.bridge_layout = import_map_data(self.Level_data["Bridge"])
        self.coconut_layout = import_map_data(self.Level_data["Coconut"])
        self.background_layout = import_map_data(self.Level_data["Background"])

        # set up the images
        self.terrain_image = import_complicated_full_sprite_sheet(Level_graphics["Sand"], tile_size, tile_size)
        self.tree_image = import_complicated_full_sprite_sheet(Level_graphics["Tree"], tile_size, tile_size)
        self.water_image = import_complicated_full_sprite_sheet(Level_graphics["Water"], tile_size, tile_size)
        self.clouds_image = import_complicated_full_sprite_sheet(Level_graphics["Clouds"], tile_size, tile_size)
        self.bridge_image = import_complicated_full_sprite_sheet(Level_graphics["Bridge"], tile_size, tile_size)
        
        # collectables
        self.coconut_image = import_complicated_full_sprite_sheet(Level_graphics["Coconut"], 14, 14)
        self.background_image = import_complicated_full_sprite_sheet(Level_graphics["Background"], tile_size, tile_size)

        # Set up the sprites
        self._create_terrain(self.background_layout, "background", self.background_image)
        self.player = self._create_player(self.player_layout)
        self._create_terrain(self.coconut_layout, "coconut", self.coconut_image)
        self._create_terrain(self.tree_layout, "tree", self.tree_image)
        self._create_terrain(self.bridge_layout, "bridge", self.bridge_image)
        self._create_terrain(self.terrain_layout, "terrain", self.terrain_image)
        self._create_terrain(self.clouds_layout, "clouds", self.clouds_image)
        
        self._create_terrain(self.water_layout, "water", self.water_image)
        

        # Level won?
        self.won = False

    def run(self, event_list, music):
        if self.player.dead:
            music.play_song("dead")
            return True

        if self.player.won:
            music.stop_song()
            music.play_song("swon")
            
            self.data[self.level_number]["completed"] = "yes"
            if self.player.collected > self.data[self.level_number]["coconuts_collected"]:
                self.data[self.level_number]["coconuts_collected"] = self.player.collected
            if self.player.speedrunner/1000 > 1 and self.player.speedrunner/1000 < self.data[self.level_number]["Best Time"] or self.data[self.level_number]["Best Time"]==0:
                self.data[self.level_number]["Best Time"] = self.player.speedrunner/1000

            with open('data.txt', 'w') as f:
                json.dump(self.data, f)
            self.won = True
    
        self.camera_group.custom_draw(self.player)
        self.water_group.update()
        self.player_group.update(event_list, music)
        self.animated_group.update()
        self.sand_group.update()

    def _create_player(self, layout):
        for row_index, row in enumerate(layout):
                for col_index, value in enumerate(row):
                    if value != '-1':
                        if value == '0':
                            y = row_index *tile_size
                            x = col_index *tile_size
                            return Player([self.player_group, self.camera_group], (x, y), self.collision_group, self.water_group, self.tree_group, self.bridge_group, self.sand_group, self.coconut_group)
     
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
                                WaterTile([self.camera_group, self.water_group], (x, y), image[int(value)], 1.05)
                            if type == "clouds":
                                StaticTile([self.camera_group], (x, y), image[int(value)])
                            if type == "bridge":
                                StaticTile([self.camera_group, self.bridge_group], (x, y), image[int(value)])
                            if type == "coconut":
                                StaticTile([self.camera_group, self.coconut_group], (x+32, y+64-14), image[int(value)])
                            if type == "background":
                                AnimatedTile([self.camera_group, self.animated_group], (x, y), image)
 
class LevelFive:
    def __init__(self):
        
        # Get the current surface
        self.surface = pygame.display.get_surface()

        
        # Level data
        self.level_number = "Level_Five"
        self.Level_data = Level_5
        self.data = {
            "Tutorial": {
                "Best Time": 0,
                "coconuts_collected": 0,
                "max_coconuts": 3,
                "completed": "no"
            },
            "Level_One": {
                "Best Time": 0,
                "coconuts_collected": 0,
                "max_coconuts": 3,
                "completed": "no"
            },
            "Level_Two": {
                "Best Time": 0,
                "coconuts_collected": 0,
                "max_coconuts": 3,
                "completed": "no"
            },
            "Level_Three": {
                "Best Time": 0,
                "coconuts_collected": 0,
                "max_coconuts": 3,
                "completed": "no"
            },
            "Level_Four": {
                "Best Time": 0,
                "coconuts_collected": 0,
                "max_coconuts": 3,
                "completed": "no"
            },
            "Level_Five": {
                "Best Time": 0,
                "coconuts_collected": 0,
                "max_coconuts": 3,
                "completed": "no"
            }
        }
        try:
            with open('data.txt') as f:
                self.data = json.load(f)
        except:
            with open('data.txt', 'w') as f:
                json.dump(self.data, f)


        # Initialize the sprite groups
        self.player_group = pygame.sprite.GroupSingle()
        self.collision_group = pygame.sprite.Group()
        self.water_group = pygame.sprite.Group()
        self.camera_group = Camera()
        self.power_group = pygame.sprite.Group()
        self.tree_group = pygame.sprite.Group()
        self.bridge_group = pygame.sprite.Group()
        self.sand_group = pygame.sprite.Group()
        self.coconut_group = pygame.sprite.Group()
        self.animated_group = pygame.sprite.Group()

        # Getting the layout data
        self.player_layout = import_map_data(self.Level_data["Player"])
        self.terrain_layout = import_map_data(self.Level_data["Sand"])
        self.tree_layout = import_map_data(self.Level_data["Tree"])
        self.water_layout = import_map_data(self.Level_data["Water"])
        self.clouds_layout = import_map_data(self.Level_data["Clouds"])
        self.bridge_layout = import_map_data(self.Level_data["Bridge"])
        self.coconut_layout = import_map_data(self.Level_data["Coconut"])
        self.background_layout = import_map_data(self.Level_data["Background"])

        # set up the images
        self.terrain_image = import_complicated_full_sprite_sheet(Level_graphics["Sand"], tile_size, tile_size)
        self.tree_image = import_complicated_full_sprite_sheet(Level_graphics["Tree"], tile_size, tile_size)
        self.water_image = import_complicated_full_sprite_sheet(Level_graphics["Water"], tile_size, tile_size)
        self.clouds_image = import_complicated_full_sprite_sheet(Level_graphics["Clouds"], tile_size, tile_size)
        self.bridge_image = import_complicated_full_sprite_sheet(Level_graphics["Bridge"], tile_size, tile_size)
        
        # collectables
        self.coconut_image = import_complicated_full_sprite_sheet(Level_graphics["Coconut"], 14, 14)
        self.background_image = import_complicated_full_sprite_sheet(Level_graphics["Background"], tile_size, tile_size)

        # Set up the sprites
        self._create_terrain(self.background_layout, "background", self.background_image)
        self.player = self._create_player(self.player_layout)
        self._create_terrain(self.coconut_layout, "coconut", self.coconut_image)
        self._create_terrain(self.bridge_layout, "bridge", self.bridge_image)
        self._create_terrain(self.terrain_layout, "terrain", self.terrain_image)
        self._create_terrain(self.tree_layout, "tree", self.tree_image)
        self._create_terrain(self.clouds_layout, "clouds", self.clouds_image)
        self._create_terrain(self.water_layout, "water", self.water_image)
        

        # Level won?
        self.won = False

    def run(self, event_list, music):
        if self.player.dead:
            music.play_song("dead")
            return True

        if self.player.won:
            music.stop_song()
            music.play_song("swon")
            
            self.data[self.level_number]["completed"] = "yes"
            if self.player.collected > self.data[self.level_number]["coconuts_collected"]:
                self.data[self.level_number]["coconuts_collected"] = self.player.collected
            if self.player.speedrunner/1000 > 1 and self.player.speedrunner/1000 < self.data[self.level_number]["Best Time"] or self.data[self.level_number]["Best Time"]==0:
                self.data[self.level_number]["Best Time"] = self.player.speedrunner/1000

            with open('data.txt', 'w') as f:
                json.dump(self.data, f)
            self.won = True
    
        self.camera_group.custom_draw(self.player)
        self.water_group.update()
        self.player_group.update(event_list, music)
        self.animated_group.update()
        self.sand_group.update()



    def _create_player(self, layout):
        for row_index, row in enumerate(layout):
                for col_index, value in enumerate(row):
                    if value != '-1':
                        if value == '0':
                            y = row_index *tile_size
                            x = col_index *tile_size
                            return Player([self.player_group, self.camera_group], (x, y), self.collision_group, self.water_group, self.tree_group, self.bridge_group, self.sand_group, self.coconut_group)
    
    
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
                                WaterTile([self.camera_group, self.water_group], (x, y), image[int(value)], 1)
                            if type == "clouds":
                                StaticTile([self.camera_group], (x, y), image[int(value)])
                            if type == "bridge":
                                StaticTile([self.camera_group, self.bridge_group], (x, y), image[int(value)])
                            if type == "coconut":
                                StaticTile([self.camera_group, self.coconut_group], (x+32, y+64-14), image[int(value)])
                            if type == "background":
                                AnimatedTile([self.camera_group, self.animated_group], (x, y), image)
 