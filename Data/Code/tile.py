import pygame
from Data.Code.settings import *
from Data.Code.helper import *
import random

class StaticTile(pygame.sprite.Sprite):
    def __init__(self, group, pos, image):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect(topleft = pos)
        self.mask = pygame.mask.from_surface(self.image)

class WaterTile(pygame.sprite.Sprite):
    def __init__(self, group, pos, image, speed):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect(topleft = pos)
        self.speed = speed
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

class SandTile(pygame.sprite.Sprite):
    def __init__(self, group, pos, image):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect(topleft = pos)
        self.touched = False
        self.shake_timer = 0
        self.offset = pygame.math.Vector2()
        self.pos = pos
        self.init_fall = False
        self.gravity = 5
        self.groups = group
    
    def shake(self):
        if self.touched and not self.init_fall:
            self.offset.y = random.randint(-1,1)
            self.offset.x = random.randint(-1,1)
            self.rect.center += self.offset
            self.shake_timer += 0.3
            if self.shake_timer > 10:
                self.init_fall = True
                self.touched = False
    
    def move(self):
        self.rect.centery += self.gravity
        
    def update(self):
        if self.init_fall:
            self.move()
            self.remove(self.groups[0])
        self.shake()
        if self.rect.centery > self.pos[1] + 400:
            self.kill()
        
class Particles(pygame.sprite.Sprite):
    pass

class MenuTile(pygame.sprite.Sprite):
    def __init__(self, group, pos, image):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect(topleft = pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.clicked = False
    
    def mouse_collision(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
            else: self.clicked = False

    def update(self):
        self.mouse_collision()

class LevelTile(MenuTile):
    def __init__(self, group, pos, image):
        super().__init__(group, pos, image)
        #self.image = pygame.transform.scale(self.image, (128, 128))
        self.display_your_data = False

    def mouse_collision(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
            else: self.clicked = False

            if pygame.mouse.get_pressed()[1]:
                self.display_your_data = True
        
