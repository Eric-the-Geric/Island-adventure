import pygame
from Data.Code.settings import *
#from Data.Code.levels import *

class Game:

    def __init__(self):
        self.surface = pygame.display.set_mode(screen)
        #self.level = Test_level()
        self.run = True
        self.clock = pygame.time.Clock()

    def loop(self):
        pygame.display.set_caption("Island Ascension")

        while self.run:
            self.surface.fill("black")
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    self.run = False
                    
            self.clock.tick(FPS)
            pygame.display.flip()
        


if __name__ == '__main__':
    game = Game()
    game.loop()