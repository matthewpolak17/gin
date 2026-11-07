import pygame

class UI_Text:

    def __init__(self, context):
        self.context = context
        self.large_font = pygame.font.Font(None, 50)
        self.medium_font = pygame.font.Font(None, 35)
        self.small_font = pygame.font.Font(None, 30)
        self.title_size = 140
        self.title_font = pygame.font.Font('./assets/fonts/DEVROYSC.ttf', round(self.title_size))

        self.dev_small_font = pygame.font.Font('./assets/fonts/DEVROYSC.ttf', 30)
        self.dev_medium_font = pygame.font.Font('./assets/fonts/DEVROYSC.ttf', 35)
        self.dev_large_font = pygame.font.Font('./assets/fonts/DEVROYSC.ttf', 50)


    def render_small(self, text, color=(255,222,133)):
        return self.small_font.render(text, True, color)
    
    def render_medium(self, text, color=(255, 222, 133)):
        return self.medium_font.render(text, True, color)
    
    def render_large(self, text, color=(255, 222, 133)):
        return self.large_font.render(text, True, color)
    
    def render_title(self, text, color=(255,222,133)):
        return self.title_font.render(text, True, color)

    def render_dev_small(self, text, color=(255,222,133)):
        return self.dev_small_font.render(text, True, color)

    def render_dev_medium(self, text, color=(255,222,133)):
            return self.dev_medium_font.render(text, True, color)
    
    def render_dev_large(self, text, color=(255,222,133)):
            return self.dev_large_font.render(text, True, color)
        