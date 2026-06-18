import pygame

class UI_Text:
    

    def __init__(self):
        self.large_font = pygame.font.Font(None, 50)
        self.medium_font = pygame.font.Font(None, 35)
        self.small_font = pygame.font.Font(None, 30)


    def render_small(self, text, color=(255, 222, 133)):
        return self.small_font.render(text, True, color)
    
    def render_medium(self, text, color=(255, 222, 133)):
        return self.medium_font.render(text, True, color)
    
    def render_large(self, text, color=(255, 222, 133)):
        return self.large_font.render(text, True, color)