import pygame
import csv
from Data.Code.settings import *
import json

def import_map_data(path):

    temp_list = []
    with open(path) as file:
        rows = csv.reader(file)
        for row in rows:
            temp_list.append(row)

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