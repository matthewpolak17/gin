import pygame

class Mixer:
    def __init__(self):
        pygame.mixer.init()

        self.CONN_INTRO_LENGTH = 92168

        self.thwip_sounds = [
            pygame.mixer.Sound("./assets/sfx/thwip3.wav"),
            pygame.mixer.Sound("./assets/sfx/thwip4.wav"),
            pygame.mixer.Sound("./assets/sfx/thwip5.wav"),
            ]
        self.shuffle_sound = pygame.mixer.Sound("./assets/sfx/shuffle.wav")
        self.slide_sound = pygame.mixer.Sound("./assets/sfx/slide1.wav")
    
    def start_networking_music(self):
        pygame.mixer.music.load("./assets/music/connecting_middle.ogg")
        pygame.mixer.music.play(-1, 0, 2000)

    def current_pos(self):
        return pygame.mixer.music.get_pos()
    
    def start_fadeout(self, time):
        pygame.mixer.music.fadeout(time)
        