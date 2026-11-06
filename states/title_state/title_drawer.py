import pygame
import math

class TitleDrawer:
    def __init__(self, context):
        self.context = context
        self.counter = 0

    def draw_cursor(self, cursor, mouse_x, mouse_y):
        if cursor:
            self.context.surface_loader.title_surface.blit(cursor, (mouse_x, mouse_y))

    def draw_title_text(self):
        surface = self.context.text_renderer.title_text
        x = (self.context.screen.display_width - surface.get_width()) // 2
        y = (self.context.screen.display_height - surface.get_height()) * 5/12
        self.context.surface_loader.title_surface.blit(surface, (x, y))

    def draw_title_background(self):
        frame = self.context.animator.title_background.frame
        self.context.surface_loader.title_surface.blit(self.context.image_loader.title_background, (-frame, 0))
        self.context.surface_loader.title_surface.blit(self.context.image_loader.title_background, (-frame + self.context.image_loader.title_background_width, 0))  
        self.context.surface_loader.title_surface.blit(self.context.text_renderer.start_text, self.context.rects.start_rect)
        self.context.surface_loader.title_surface.blit(self.context.text_renderer.multiplayer_text, self.context.rects.multiplayer_rect)
    