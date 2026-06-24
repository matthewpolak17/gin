import pygame

class UI_Text:

    def __init__(self):
        self.large_font = pygame.font.Font(None, 50)
        self.medium_font = pygame.font.Font(None, 35)
        self.small_font = pygame.font.Font(None, 30)
        self.title_size = 140
        self.title_font = pygame.font.Font('./assets/fonts/Mermaid1001.ttf', round(self.title_size))


    def render_small(self, text, color=(255,222,133)):
        return self.small_font.render(text, True, color)
    
    def render_medium(self, text, color=(255, 222, 133)):
        return self.medium_font.render(text, True, color)
    
    def render_large(self, text, color=(255, 222, 133)):
        return self.large_font.render(text, True, color)
    
    def render_title(self, text, color=(255,222,133)):
        return self.title_font.render(text, True, color)
    
    def update_title_size(self, frame, anim_frames):
        factor = frame / anim_frames
        exponential = 1 - (1-factor) ** 2
        self.title_size = 140 + 40 * exponential
        self.title_font = pygame.font.Font('./assets/fonts/Mermaid1001.ttf', round(self.title_size))

    def update_title_alpha(self, title_text, frame, anim_frames):
        factor = frame / anim_frames
        exponential = 1 - (1-factor) ** 2
        alpha = (255 * (1 - exponential))
        title_text.set_alpha(alpha)
        