import pygame

class SoundEffects:
    def __init__(self):
        pygame.mixer.init()
        
        # Sounds
        self.coconut = pygame.mixer.Sound("Data/Audio/Coconut.wav")
        self.dafluffy = pygame.mixer.Sound("Data/Audio/Dafluffy.wav")
        self.dead = pygame.mixer.Sound("Data/Audio/Dead.wav")
        self.jump = pygame.mixer.Sound("Data/Audio/Jump.wav")
        self.main_loop = pygame.mixer.Sound("Data/Audio/Main loop.wav")
        self.sand = pygame.mixer.Sound("Data/Audio/Sand.wav")
        self.tutorial = pygame.mixer.Sound("Data/Audio/Tutorial.wav")
        self.water = pygame.mixer.Sound("Data/Audio/water.wav")
        self.won = pygame.mixer.Sound("Data/Audio/won.wav")
        self.short_won = pygame.mixer.Sound("Data/Audio/short_won.wav")

        self.sound_dictionary = {"coc": self.coconut,
                                 "da": self.dafluffy,
                                 "jump": self.jump,
                                 "menu": self.main_loop,
                                 "sand": self.sand,
                                 "tut": self.tutorial,
                                 "water": self.water,
                                 "dead": self.dead,
                                 "won": self.won,
                                 "swon": self.short_won}
    
    def play_song(self, song_key, volume = 0.1, boolean = False):

        sound = self.sound_dictionary[song_key]
        sound.set_volume(volume)
        if boolean:
            sound.play(-1)
        else:
            sound.play()

    def stop_song(self):
        for key in self.sound_dictionary.keys():
            self.sound_dictionary[key].stop()