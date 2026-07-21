import pygame

class ImageLoader:
    def __init__(self, context):
        self.context = context

        self.blue_back = pygame.transform.scale(pygame.image.load(r'./assets/images/blueback.png'), (73, 98))
        self.card_images = {}

        self.set_card_images(self.context.card_data)
        self.set_background()
        self.set_networking_background()
        self.set_title_background()
        self.set_loading_images()
        self.set_card_border_frames()
        self.set_icon()

    def set_icon(self):
        self.icon = pygame.image.load(f'./assets/images/icon.png').convert_alpha()
        pygame.display.set_icon(self.icon)

    def set_background(self):
        self.background = pygame.image.load(r'./assets/images/background.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (self.context.screen.display_width, self.context.screen.display_height))

    def set_networking_background(self):
        self.networking_background = pygame.image.load(r'./assets/images/black.png').convert_alpha()
        self.networking_background = pygame.transform.scale(self.networking_background, (self.context.screen.display_width, self.context.screen.display_height))

    def set_title_background(self):
        self.title_background = pygame.image.load(f'./assets/images/title_background.png').convert_alpha()
        self.title_background = pygame.transform.scale(self.title_background, (self.context.screen.display_width, self.context.screen.display_height))
        self.title_background_width = self.title_background.get_width()

    def set_card_images(self, card_data):
        for name in card_data:
            img = pygame.image.load(f'./assets/cards/{name}').convert_alpha()
            self.card_images[name] = pygame.transform.smoothscale(img, (self.context.constants.CARD_WIDTH, self.context.constants.CARD_HEIGHT))

    def set_loading_images(self):
        self.loading_frames = []
        for i in range(12):
            image = pygame.image.load(f"./assets/images/loading_frames/loading_frame_{i}.png").convert_alpha()
            image = pygame.transform.smoothscale(image, (self.context.screen.display_width // 50, self.context.screen.display_width // 50)) #width x width
            self.loading_frames.append(image)
    
    def set_card_border_frames(self):
        self.spirit_card_border_frames = []
        for i in range(10):
            image = pygame.image.load(f"./assets/images/card_border_frames/spirit_border_frames/spirit_frame_{i}.png").convert_alpha()
            self.spirit_card_border_frames.append(image)

        self.rainbow_card_border_frames = []
        for i in range(24):
            image = pygame.image.load(f"./assets/images/card_border_frames/rainbow_border_frames/rainbow_frame_{i}.png").convert_alpha()
            self.rainbow_card_border_frames.append(image)