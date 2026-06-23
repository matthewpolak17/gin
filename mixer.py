import pygame

class Mixer:
    def __init__(self):
        pygame.mixer.init()
        self.thwip_sounds = [
            pygame.mixer.Sound("./assets/sfx/thwip3.wav"),
            pygame.mixer.Sound("./assets/sfx/thwip4.wav"),
            pygame.mixer.Sound("./assets/sfx/thwip5.wav"),
            ]
        self.shuffle_sound = pygame.mixer.Sound("./assets/sfx/shuffle.wav")
        self.slide_sound = pygame.mixer.Sound("./assets/sfx/slide1.wav")

        #self.networking_loop = pygame.mixer.music.load("./assets/music/connecting_middle.wav")
        #self.networking_intro = pygame.mixer.music("./assets/music/connecting_start.wav")

    def play_menu_music(self):
        pygame.mixer.music.load("./assets/music/connecting_start.wav")
        pygame.mixer.music.play()
        pygame.mixer.music.set_endevent(pygame.USEREVENT)

    def handle_music_event(self, event):
        if event.type == pygame.USEREVENT:
            pygame.mixer.music.load("./assets/music/connecting_start.wav")
            pygame.mixer.music.play(-1)