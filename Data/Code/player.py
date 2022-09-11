import pygame
from Data.Code.helper import *
from Data.Code.level_data import Level_graphics

class Player(pygame.sprite.Sprite):
    def __init__(self, group, pos, collision_group, water_group, tree_group, bridge_group, sand_group, coconut_group):
        super().__init__(group)

        
        
        # get the screen
        self.surface = pygame.display.get_surface()

        self.h_width = self.surface.get_size()[0]//2
        self.h_height = self.surface.get_size()[1]//2
        self.offset= pygame.math.Vector2()

        # get which groups the player belongs to. for handling deaths
        self.group = group
        # For handling player movements
        self.pos = pos
        self.direction = pygame.math.Vector2()
        self.speed = 3
        self.gravity = 0.15
        self.jump_height = -5
        self.jumps = 0
        self.max_jumps = 1
        self.collected = 0
        


        # Player graphics
        self.idle = import_complicated_full_sprite_sheet(Level_graphics["Player_idle"], player_size, player_size)
        self.walking_right = import_complicated_full_sprite_sheet(Level_graphics["Player_walking"], player_size, player_size)
        self.jumping = import_complicated_full_sprite_sheet(Level_graphics["Player_jumping"], player_size, player_size)

        # Player hitbox and image
        self.image = self.idle[0]
        self.rect = self.image.get_rect(topleft=pos)
        self.mask = pygame.mask.from_surface(self.image)

            #collisions
        self.collision_group = collision_group
        self.water_group = water_group
        self.tree_group = tree_group
        self.bridge_group = bridge_group
        self.sand_group = sand_group
        self.coconut_group = coconut_group

        # Player animation

        self.frames = 0
        self.action = "right"
        self.frame_speed = 0.05

        # Interactions

        self.underwater = False
        self.max_breath = 300
        self.breath = 300
        self.dead = False
        self.won = False
        self.speedrunner = 0
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
            if event.type == pygame.USEREVENT:
                # time in ms
                self.speedrunner += 1
    def move(self):
        if self.direction.magnitude() != 0:
            self.direction.normalize()
        self.rect.center += self.direction*self.speed
    
    def animate(self):
        if self.direction.y > 2 and self.action == "right":
            self.image = self.jumping[3]

        elif self.direction.y > 2 and self.action == "left":
            self.image = pygame.transform.flip(self.jumping[3], True, False)

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
            self.gravity = 0.075
            self.speed = 2.7
            
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
                if self.direction.y > 8 and abs(self.rect.bottom - sprite.rect.top) < 60:
                    self.rect.bottom = sprite.rect.top
                    self.direction.y = 0
                    self.jumps = 0
                elif self.direction.y > 0 and abs(self.rect.bottom - sprite.rect.top) < 50:
                    self.rect.bottom = sprite.rect.top
                    self.direction.y = 0
                    self.jumps = 0
    
                if self.direction.y < 0:
                    self.rect.top = sprite.rect.bottom
                    self.direction.y = 0

    def water_collision(self):
        for sprite in self.water_group.sprites():
            if sprite.rect.top < self.rect.centery:
                self.underwater = True
                self.all_blue()
                break
            elif sprite.rect.bottom > self.rect.centery:
                self.underwater = False
                self.all_blue()
                break

    def all_blue(self):
        if self.underwater:
            for sprite in self.water_group.sprites():
                sprite.collision = True
        if not self.underwater:
            for sprite in self.water_group.sprites():
                sprite.collision = False
    def drowning(self):
        if self.underwater:
            self.breath -= 1
        elif not self.underwater and self.breath < self.max_breath:
            self.breath+=2

    def kill_player(self):
        if self.breath <= 0:
            self.dead = True
    def breath_bar(self):
        self.offset.x += (self.rect.right - 100 - self.offset.x - (screen_width)//2)
        self.offset.y += (self.rect.centery - 280 - self.offset.y - (screen_height)//2)
        offset_pos = (self.rect.topleft - self.offset)
        pygame.draw.rect(self.surface, ("white"), pygame.Rect(offset_pos[0], offset_pos[1], self.breath, 10))

    def win_level(self):
        for sprite in self.tree_group:
            if sprite.rect.colliderect(self.rect):
                self.won = True

    def Bridge_collision(self):
        for sprite in self.bridge_group.sprites():
            if sprite.rect.colliderect(self.rect):
                
                if self.direction.y > 5.5 and abs(self.rect.bottom - sprite.rect.top) < 42:
                    self.rect.bottom = sprite.rect.top
                    self.direction.y = 0
                    self.jumps = 0
                elif self.direction.y > 0 and abs(self.rect.bottom - sprite.rect.top) < 25:
                    self.rect.bottom = sprite.rect.top
                    self.direction.y = 0
                    self.jumps = 0

    def Sand_collision(self):
        for sprite in self.sand_group.sprites():
            if sprite.rect.colliderect(self.rect):
                sprite.touched = True

    def Coconut_collision(self):
        for sprite in self.coconut_group.sprites():
             if sprite.rect.colliderect(self.rect):
                    self.collected += 1
                    sprite.kill()

    def update(self, event_list):
        self.get_input(event_list)
        self.move()
        self.Sand_collision()
        self.horizontal_collision()
        self.apply_gravity()
        self.vertical_collision()
        self.Bridge_collision()
        self.animate()
        self.water_collision()
        self.Coconut_collision()
        self.breath_bar()
        self.drowning()
        self.kill_player()
        self.win_level()