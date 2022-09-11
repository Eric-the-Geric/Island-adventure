import pygame
from Data.Code.settings import *
from Data.Code.levels import *
import sys
class Tutorial:

    def __init__(self):
        pygame.init()

        # with the flags arguments it makes it so I can toggle full-screen
        self.surface = pygame.display.set_mode(screen, flags=pygame.SCALED)
        
        self.run = True
        self.clock = pygame.time.Clock()
        self.level = Test_level()
        self.font = pygame.font.Font(None, 30)
        self.fps_offset = pygame.math.Vector2()

        
    def loop(self):
        pygame.time.set_timer(pygame.USEREVENT, 1)

        pygame.display.set_caption("Island Ascension")
        while self.run:
            
            self.surface.fill("black")
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    self.run = False
                    pygame.quit()
                    sys.exit()
                if event.type ==pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        menu = Menu()
                        menu.loop()
                        #self.run = False
                    if event.key == pygame.K_f:
                        pygame.display.toggle_fullscreen()
                    if event.key ==pygame.K_r:
                        self.level = Test_level()
   
            if self.level.run(events):
                menu = Menu()
                menu.loop()
                # self.run = False
                    
            if self.level.won:
                menu = Menu()
                menu.loop()
                # self.run = False

            self.clock.tick(FPS)
            self.display_fps()
            self.display_clock()
            pygame.display.flip()
        
    def display_fps(self):
        text = self.font.render("FPS: " + str(int(self.clock.get_fps())), True, ("white"))
        textRect = text.get_rect()
        self.fps_offset.x += (self.level.player.rect.centerx + 240 - self.fps_offset.x - (screen_width)//2)
        self.fps_offset.y += (self.level.player.rect.centery + 280 - self.fps_offset.y - (screen_height)//2)
        textRect.center = (self.level.player.rect.topleft - self.fps_offset)
        self.surface.blit(text, textRect)
    
    def display_clock(self):
        text = self.font.render("time: " + str(self.level.player.speedrunner/1000), True, ("white"))
        textRect = text.get_rect()
        self.fps_offset.x += (self.level.player.rect.centerx - 240 - self.fps_offset.x - (screen_width)//2)
        self.fps_offset.y += (self.level.player.rect.centery + 280 - self.fps_offset.y - (screen_height)//2)
        textRect.center = (self.level.player.rect.topleft - self.fps_offset)
        self.surface.blit(text, textRect)
        
class Menu:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode(screen, flags=pygame.SCALED)
        self.run = True
        self.clock = pygame.time.Clock()
        self.level = Main_menu()
        self.tutorial = False
        self.keybindings = False
        self.quit = False
        self.fluffy = False
        self.level_selector = False
        self.tutorial = Tutorial()

    def loop(self):
        pygame.display.set_caption("Island Ascension")
        while self.run:
            
            self.surface.fill("white")
            events = pygame.event.get()
            self.level.run()
            for event in events:
                if event.type == pygame.QUIT:
                    self.run = False
                    pygame.quit()
                    sys.exit()
                if event.type ==pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.quit = True
                        self.run = False
                    if event.key == pygame.K_f:
                        pygame.display.toggle_fullscreen()
            if self.level.Tutorial.sprite.clicked:
                self.level.Tutorial.sprite.clicked = not self.level.Tutorial.sprite.clicked 
                self.tutorial.loop()
                
            if self.level.key_bindings.sprite.clicked:
                self.keybindings = True
                
            if self.level.fluffy.sprite.clicked:
                self.fluffy = True
                
            if self.level.quit.sprite.clicked:
                self.quit= True
                self.run = False
                pygame.quit()
                sys.exit()
            if self.level.Level_selection.sprite.clicked:
                self.level_selector = True
                

            self.clock.tick(FPS)
            pygame.display.flip()

def main():
    menu = Menu()
    menu.loop()
if __name__ == '__main__':
    main()