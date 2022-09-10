import pygame
from Data.Code.helper import *
from Data.Code.level_data import Level_graphics

class Player(pygame.sprite.Sprite):
    def __init__(self, group, pos, collision_group, water_group):
        super().__init__(group)

        # get the screen
        self.surface = pygame.display.get_surface()

        # get which groups the player belongs to. for handling deaths
        self.group = group
        # For handling player movements
        self.pos = pos
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.gravity = 0.15
        self.jump_height = -3
        self.jumps = 0
        self.max_jumps = 1
        self.score = 0

        # Player graphics
        self.idle = import_complicated_full_sprite_sheet(Level_graphics["Player_idle"], player_size, player_size)
        self.walking_right = import_complicated_full_sprite_sheet(Level_graphics["Player_walking"], player_size, player_size)
        self.jumping = import_complicated_full_sprite_sheet(Level_graphics["Player_jumping"], player_size, player_size)

        # Player hitbox and image
        self.image = self.idle[0]
        self.rect = self.image.get_rect(topleft=pos)
        
            #collisions
        self.collision_group = collision_group
        self.water_group = water_group
        # Player animation

        self.frames = 0
        self.action = "right"
        self.frame_speed = 0.1

        # Interactions

        self.underwater = False
        self.breath = 100

    def get_input(self, events):
        keys = pygame.key.get_pressed()
        self.frames += self.frame_speed
        if keys[pygame.K_ESCAPE]:
            self.pause = True

        # Horizontal
        if keys[pygame.K_a]:
            self.direction.x = -1
            self.action = "left"
            
        elif keys[pygame.K_d]:
            self.direction.x = 1
            self.action = "right"
        else:
            self.direction.x = 0
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.jumps < self.max_jumps:
                    self.direction.y = self.jump_height
                    self.image = self.jumping[0]
                    self.jumps += 1
    def move(self):
        if self.direction.magnitude() != 0:
            self.direction.normalize()
        self.rect.center += self.direction*self.speed
    
    def animate(self):
        if self.direction.y > 0.5 and self.action == "right":
            self.image = self.jumping[2]

        elif self.direction.y > 0.5 and self.action == "left":
            self.image = pygame.transform.flip(self.jumping[2], True, False)

        elif self.direction.x == 0 and self.action == "right":
            self.image = self.idle[int(self.frames) % 2]
        
        elif self.direction.x == 0 and self.action == "left":
            self.image = pygame.transform.flip(self.idle[int(self.frames) % 2], True, False)
            
        elif self.direction.x > 0 and self.action == "right":
            self.image = self.walking_right[int(self.frames)%3]

        elif self.direction.x < 0 and self.action == "left":
            self.image = pygame.transform.flip(self.walking_right[int(self.frames)%3], True, False)


    def apply_gravity(self):
        if self.underwater:
            self.gravity = 0.01
            self.speed = 1
            self.jump_height = -1
        else:
            self.gravity = 0.15
            self.speed = 5
            self.jump_height = -3
            
        self.direction.y += self.gravity


    def horizontal_collision(self):
        for sprite in self.collision_group.sprites():
            if sprite.rect.colliderect(self.rect):
                if self.direction.x < 0 and abs(self.rect.left - sprite.rect.right) < 10:
                    self.rect.left = sprite.rect.right


                if self.direction.x > 0 and abs(self.rect.right - sprite.rect.left) < 10:
                    self.rect.right = sprite.rect.left

    def vertical_collision(self):
        for sprite in self.collision_group.sprites():
            if sprite.rect.colliderect(self.rect):
                if self.direction.y > 0:
                    self.rect.bottom = sprite.rect.top
                    self.direction.y = 0
                    self.jumps = 0
    
                if self.direction.y < 0:
                    self.rect.top = sprite.rect.bottom
                    self.direction.y = 0

    def water_collision(self):
        for sprite in self.water_group.sprites():
            if sprite.rect.colliderect(self.rect):
                self.underwater = True
                self.deep_blue()
            else: 
                
                self.underwater = False

    def deep_blue(self):
        if self.underwater:
            for sprite in self.water_group.sprites():
                sprite.collision = True
        if not self.underwater:
            for sprite in self.water_group.sprites():
                sprite.collision = False
                

    def update(self, event_list):
        self.get_input(event_list)
        self.move()
        self.horizontal_collision()
        self.apply_gravity()
        self.vertical_collision()
        self.animate()
        self.water_collision()
        #self.deep_blue()