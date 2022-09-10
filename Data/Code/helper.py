import pygame
import csv
from Data.Code.settings import *


def import_map_data(path):

    temp_list = []
    with open(path) as file:
        rows = csv.reader(file)
        for row in rows:
            temp_list.append(row)

    return temp_list


def import_images(path):
    
    temp_list = []
    image = pygame.image.load(path).convert_alpha()
    image_width = image.get_width()
    number_tiles = image_width//tile_size

    for i in range(number_tiles):
        new_image = image.subsurface(pygame.Rect(i*tile_size, 0, tile_size, tile_size))
        transformed_image = pygame.transform.scale(new_image, (tile_size, tile_size))
        temp_list.append(transformed_image)

    return temp_list
    

def import_full_sprite_sheet(path):
    temp_list = []
    image = pygame.image.load(path).convert()
    
    #sets pixels of this colour to be tramsparent. Then you also need to call convert() not convert_alpha
    image.set_colorkey((0,0,0))
    
    # image.set_alpha(255) --> sets the transparency of the whole image
    image_width = image.get_width()
    image_height = image.get_height()
    rows = image_height // 8
    cols = image_width // 8

    for i in range(rows):
        for j in range(cols):
            new_image = image.subsurface(pygame.Rect(i*8, j*8, 8, 8))
            transformed_image = pygame.transform.scale(new_image, (8*8, 8*8))
            temp_list.append(transformed_image)

    return temp_list

def import_complicated_full_sprite_sheet(path, tile_width, tile_height):
    temp_list = []
    image = pygame.image.load(path).convert()
    
    #sets pixels of this colour to be tramsparent. Then you also need to call convert() not convert_alpha
    image.set_colorkey(colour_key)
    
    # image.set_alpha(255) --> sets the transparency of the whole image
    image_width = image.get_width()
    image_height = image.get_height()
    rows = image_height // tile_height
    cols = image_width // tile_width

    for i in range(rows):
        for j in range(cols):
            
            left = i*tile_height
            top = j *tile_width
            new_image = image.subsurface(pygame.Rect(top, left, tile_width, tile_height))
            temp_list.append(new_image)

    return temp_list