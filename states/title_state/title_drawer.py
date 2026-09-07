import pygame
import math

class TitleDrawer:
    def __init__(self, context):
        self.context = context
        self.counter = 0
    
    def draw_coin_frame(self):
        frame = self.context.image_loader.coin_frames[self.context.title_animator.coin.frame]
        coin_rect = frame.get_rect(center=(self.context.screen.display_width - 2*frame.get_width(), self.context.screen.display_height - 2*frame.get_height()))
        self.context.surface_loader.title_surface.blit(frame, coin_rect)

        count_text = self.context.text_renderer.coin_text
        text_rect = count_text.get_rect(midbottom=(coin_rect.centerx, coin_rect.top - coin_rect.height //4))
        self.context.surface_loader.title_surface.blit(count_text, text_rect)

    def draw_lucky_coin_frame(self):
        frame = self.context.image_loader.lucky_coin_frames[self.context.title_animator.lucky_coin.frame]
        coin_rect = frame.get_rect(center=(self.context.screen.display_width - 4*frame.get_width(), self.context.screen.display_height - 2*frame.get_height()))
        self.context.surface_loader.title_surface.blit(frame, coin_rect)

        count_text = self.context.text_renderer.lucky_coin_text
        text_rect = count_text.get_rect(midbottom=(coin_rect.centerx, coin_rect.top - coin_rect.height //4))
        self.context.surface_loader.title_surface.blit(count_text, text_rect)

    def draw_cursor(self, cursor, mouse_x, mouse_y):
        if cursor:
            self.context.surface_loader.title_surface.blit(cursor, (mouse_x, mouse_y))