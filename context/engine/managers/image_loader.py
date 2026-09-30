import pygame

class ImageLoader:
    def __init__(self, context):
        self.context = context
        self.card_size = (
            round(self.context.constants.CARD_WIDTH * self.context.screen.scale),
            round(self.context.constants.CARD_HEIGHT * self.context.screen.scale),
        )
        self.blue_back = pygame.transform.scale(pygame.image.load(r'./assets/images/blueback.png'), self.card_size)
        self.card_images = {}

        self.set_card_images(self.context.card_data)
        self.set_background()
        self.set_ui_elements()
        self.set_networking_background()
        self.set_title_background()
        self.set_loading_images()
        self.set_coin_frames()
        self.set_lucky_coin_frames()
        self.set_card_border_frames()
        self.set_icon()
        self.set_cursors()

    def set_icon(self):
        self.icon = pygame.image.load(f'./assets/images/icon.png').convert_alpha()
        pygame.display.set_icon(self.icon)

    def set_background(self):
        self.background = pygame.image.load(r'./assets/images/background.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (self.context.screen.display_width, self.context.screen.display_height))

    def set_ui_elements(self):
        self.button = pygame.image.load(r'./assets/images/ui/ui_button.png').convert_alpha()
        self.button =  self.scale_image(self.button, 0.35)

        self.pressed_button = pygame.image.load(r'./assets/images/ui/ui_button_pressed.png').convert_alpha()
        self.pressed_button =  self.scale_image(self.pressed_button, 0.35)

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
            image = pygame.image.load(f"./assets/images/frames/loading_frames/loading_frame_{i}.png").convert_alpha()
            image = pygame.transform.smoothscale(image, (self.context.screen.display_width // 50, self.context.screen.display_width // 50)) #width x width
            self.loading_frames.append(image)
    
    def set_card_border_frames(self):
        self.spirit_card_border_frames = []
        for i in range(10):
            image = pygame.image.load(f"./assets/images/frames/card_border_frames/spirit_border_frames/spirit_frame_{i}.png").convert_alpha()
            self.spirit_card_border_frames.append(image)

        self.rainbow_card_border_frames = []
        for i in range(24):
            image = pygame.image.load(f"./assets/images/frames/card_border_frames/rainbow_border_frames/rainbow_frame_{i}.png").convert_alpha()
            self.rainbow_card_border_frames.append(image)

    def set_coin_frames(self): 
        self.coin_frames = []
        for i in range(19):
            image = pygame.image.load(f"./assets/images/frames/coin_frames/coin_frame_{i}.png").convert_alpha()
            image = self.scale_image(image, 0.6)
            self.coin_frames.append(image)

    def set_lucky_coin_frames(self): 
            self.lucky_coin_frames = []
            for i in range(19):
                image = pygame.image.load(f"./assets/images/frames/lucky_coin_frames/lucky_coin_frame_{i}.png").convert_alpha()
                image = self.scale_image(image, 0.6)
                self.lucky_coin_frames.append(image)

    def set_cursors(self):
        self.closed_hand_cursor = pygame.image.load(f"./assets/images/cursors/closed_hand.png").convert_alpha()
        self.open_hand_cursor = pygame.image.load(f"./assets/images/cursors/open_hand.png").convert_alpha()
        self.pointing_hand_cursor = pygame.image.load(f"./assets/images/cursors/pointing_hand.png").convert_alpha()
        self.resting_cursor = pygame.image.load(f"./assets/images/cursors/resting.png").convert_alpha()

    def scale_image(self, image, scale):
        w, h = image.get_size()
        return pygame.transform.smoothscale(
            image,
            (int(w * scale), int(h * scale))
    )

    def load_pixel_art(self, path, size):
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, size)   # nearest-neighbor, keeps edges hard