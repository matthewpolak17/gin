import pygame

class Sfx:
    def __init__(self):
        pygame.mixer.init()
        self.thwip_sounds = [
            pygame.mixer.Sound("./assets/sfx/thwip3.wav"),
            pygame.mixer.Sound("./assets/sfx/thwip4.wav"),
            pygame.mixer.Sound("./assets/sfx/thwip5.wav"),
            ]
        self.shuffle_sound = pygame.mixer.Sound("./assets/sfx/shuffle.wav")
        self.slide_sound = pygame.mixer.Sound("./assets/sfx/slide1.wav")