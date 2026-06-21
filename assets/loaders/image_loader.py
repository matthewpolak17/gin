import pygame
import constants

class ImageLoader:
    def __init__(self, screen):
        self.screen = screen

        self.blue_back = pygame.transform.scale(pygame.image.load(r'./assets/blueback.png'), (73, 98))
        self.card_images = {}

        self.set_background()
        self.set_networking_background()
        self.set_title_background()
        self.set_icon()

    def set_icon(self):
        self.icon = pygame.image.load(f'./assets/icon.png').convert_alpha()
        pygame.display.set_icon(self.icon)

    def set_background(self):
        self.background = pygame.image.load(r'./assets/background.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (self.screen.display_width, self.screen.display_height))

    def set_networking_background(self):
        self.networking_background = pygame.image.load(r'./assets/networking_background.jpg').convert_alpha()
        self.networking_background = pygame.transform.scale(self.networking_background, (self.screen.display_width, self.screen.display_height))

    def set_title_background(self):
        self.title_background = pygame.image.load(f'./assets/title_background.png').convert_alpha()
        self.title_background = pygame.transform.scale(self.title_background, (self.screen.display_width, self.screen.display_height))
        self.title_background_width = self.title_background.get_width()

    def create_card_images(self, card_data):
        for name in card_data:
            img = pygame.image.load(f'./assets/cards/{name}').convert_alpha()
            self.card_images[name] = pygame.transform.smoothscale(img, (constants.CARD_WIDTH, constants.CARD_HEIGHT))
