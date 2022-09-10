import pygame

class SoundEffects:
    def __init__(self):
        pygame.mixer.init()
        
        # Sounds
        self.easter_egg_sound = pygame.mixer.Sound("Sounds/easter_egg.wav")
        self.ten_death = pygame.mixer.Sound("Sounds/10_deaths.wav")
        self.death_sound = pygame.mixer.Sound("Sounds/death_sound.wav")
        self.ending_sound = pygame.mixer.Sound("Sounds/ending.wav")
        self.main_menu_sound = pygame.mixer.Sound("Sounds/menu_song.wav")
        self.meteor_sound = pygame.mixer.Sound("Sounds/meteor.wav")
        self.introduction_sound = pygame.mixer.Sound("Sounds/instructions and intro.wav")
        self.main_game_sound = pygame.mixer.Sound("Sounds/main_main_loop.wav")

        self.sound_dictionary = {"egg":self.easter_egg_sound,
                                 "ten":self.ten_death,
                                 "death":self.death_sound,
                                 "end":self.ending_sound,
                                 "menu":self.main_menu_sound,
                                 "meteor":self.meteor_sound,
                                 "intro":self.introduction_sound,
                                 "game":self.main_game_sound}
    
    def fetch_song(self, song_key):
        sound = self.sound_dictionary[song_key]
        return sound


    def play_song(self, song_key, volume = 0.1, boolean = False):

        sound = self.sound_dictionary[song_key]
        sound.set_volume(volume)
        if boolean:
            sound.play(-1)
        else:
            sound.play()
        return sound

    def stop_song(self):
        for key in self.sound_dictionary.keys():
            self.sound_dictionary[key].stop()