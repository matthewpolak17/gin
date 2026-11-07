import pygame
import math

class ShopDrawer:
    def __init__(self, context):
        self.context = context
        self.underlay_color = (0,0,0,128)
        self.counter = 0
    
    def draw_coin_frame(self):
        frame = self.context.image_loader.coin_frames[self.context.shop_animator.coin.frame]
        coin_rect = frame.get_rect(center=(self.context.screen.display_width - 2*frame.get_width(), self.context.screen.display_height - 2*frame.get_height()))
        self.context.surface_loader.shop_surface.blit(frame, coin_rect)

        count_text = self.context.text_renderer.coin_text
        text_rect = count_text.get_rect(midbottom=(coin_rect.centerx, coin_rect.top - coin_rect.height //4))
        self.context.surface_loader.shop_surface.blit(count_text, text_rect)

    def draw_cursor(self, cursor, mouse_x, mouse_y):
        if cursor:
            self.context.surface_loader.title_surface.blit(cursor, (mouse_x, mouse_y))

    def draw_shop_background(self):
        self.context.surface_loader.shop_surface.blit(self.context.image_loader.shop_background, (0,0))

    def draw_shop_underlay(self):
        self.context.surface_loader.shop_surface.blit(self.context.surface_loader.shop_underlay_surface, (self.context.screen.display_surface.get_width() / 6, 50))

    def draw_shop_text(self):
        self.context.surface_loader.shop_surface.blit(self.context.text_renderer.shop_shop_text, self.context.text_renderer.shop_shop_text.get_rect(center=(self.context.screen.display_surface.get_width() / 2, 150)))
        self.context.surface_loader.shop_surface.blit(self.context.text_renderer.shop_buy_text, self.context.text_renderer.shop_buy_text.get_rect(center=(self.context.surface_loader.shop_underlay_surface.get_width(), 300)))