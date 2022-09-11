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

class AnimatedTile(pygame.sprite.Sprite):
    def __init__(self, group, pos, image):
        super().__init__(group)
        self.group = group
        self.image_list = image
        for image in self.image_list:
            image.set_alpha(200)
        self.image = self.image_list[0]
        self.rect = self.image.get_rect(topleft = pos)
        self.frames = random.randint(0,3)
        self.modded = len(self.image_list)
        self.animation_speed = (random.randint(0,10))/100
        self.particles = []
        self.max_particles = 2

    def animate(self):
        self.image = self.image_list[(int(self.frames) + self.modded) % self.modded]
        self.frames += self.animation_speed
    
    def update(self):
        self.animate()
    

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
        self.particles = []
    
    def shake(self):
        if self.touched and not self.init_fall:
            self.offset.y = random.randint(-1,1)
            self.offset.x = random.randint(-1,1)
            self.rect.center += self.offset
            self.particles.append(Particles(self.groups[2], self.rect.center))
            self.shake_timer += 0.3
            
            if self.shake_timer > 10:
                self.init_fall = True
                self.touched = False
    
    def move(self):
        self.rect.centery += self.gravity
        
    def update(self):
        for sprite in self.particles:
            sprite.update()
        if self.init_fall:
            self.move()
            self.remove(self.groups[0])
        self.shake()
        if self.rect.centery > self.pos[1] + 400:
            for sprite in self.particles:
                sprite.kill()
            self.kill()
        
class Particles(pygame.sprite.Sprite):
    def __init__(self, group, pos):
        super().__init__(group)
        self.image = pygame.image.load("Data/Graphics/sand(5x5).png").convert()
        self.image.set_colorkey(colour_key)
        self.speed = random.randint(1,4)
        self.direction = pygame.math.Vector2(random.uniform(-1, 1), 1).normalize()
        self.rect = self.image.get_rect(topleft = pos)

    def shoot(self):
        self.rect.center += self.direction*self.speed
    
    def update(self):
        self.shoot()

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
        self.display_your_data = False

    def mouse_collision(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
            else: self.clicked = False

            if pygame.mouse.get_pressed()[1]:
                self.display_your_data = True
    def update(self):
        self.mouse_collision()
        
