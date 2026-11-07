import pygame
import math

class ShopDrawer:
    def __init__(self, context):
        self.context = context
        self.underlay_color = (0,0,0,128)
        self.underlay_position = 1/5
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
        self.context.surface_loader.shop_surface.blit(self.context.surface_loader.shop_underlay_surface, (self.context.screen.display_surface.get_width() * self.underlay_position, 50))

    def draw_shop_text(self):
        self.context.surface_loader.shop_surface.blit(self.context.text_renderer.shop_shop_text, self.context.text_renderer.shop_shop_text.get_rect(center=(self.context.screen.display_surface.get_width() / 2, 150)))
        self.context.surface_loader.shop_surface.blit(self.context.text_renderer.shop_buy_text, self.context.text_renderer.shop_buy_text.get_rect(center=(self.context.screen.display_surface.get_width() * self.underlay_position + self.context.surface_loader.shop_underlay_surface.get_width() * 20/100, 230)))
        self.context.surface_loader.shop_surface.blit(self.context.text_renderer.shop_collection_text, self.context.text_renderer.shop_collection_text.get_rect(center=(self.context.screen.display_surface.get_width() * self.underlay_position + self.context.surface_loader.shop_underlay_surface.get_width() * 83/100, 230))) 
        #rarities
        self.context.surface_loader.shop_surface.blit(self.context.text_renderer.shop_common_text, self.context.text_renderer.shop_common_text.get_rect(center=(self.context.rects.shop_common_rect.center))) #common
        self.context.surface_loader.shop_surface.blit(self.context.text_renderer.shop_uncommon_text, self.context.text_renderer.shop_uncommon_text.get_rect(center=(self.context.rects.shop_uncommon_rect.center))) #uncommon
        self.context.surface_loader.shop_surface.blit(self.context.text_renderer.shop_rare_text, self.context.text_renderer.shop_rare_text.get_rect(center=(self.context.rects.shop_rare_rect.center))) #rare
        self.context.surface_loader.shop_surface.blit(self.context.text_renderer.shop_legendary_text, self.context.text_renderer.shop_legendary_text.get_rect(center=(self.context.rects.shop_legendary_rect.center))) #legendary
        #prices
        self.context.surface_loader.shop_surface.blit(self.context.text_renderer.shop_common_price_text, self.context.text_renderer.shop_common_price_text.get_rect(center=(self.context.screen.display_surface.get_width() * self.underlay_position + self.context.surface_loader.shop_underlay_surface.get_width() * 83/100, 230))) #$25
        self.context.surface_loader.shop_surface.blit(self.context.text_renderer.shop_uncommon_price_text, self.context.text_renderer.shop_uncommon_price_text.get_rect(center=(self.context.screen.display_surface.get_width() * self.underlay_position + self.context.surface_loader.shop_underlay_surface.get_width() * 83/100, 230))) #$100
        self.context.surface_loader.shop_surface.blit(self.context.text_renderer.shop_rare_price_text, self.context.text_renderer.shop_rare_price_text.get_rect(center=(self.context.screen.display_surface.get_width() * self.underlay_position + self.context.surface_loader.shop_underlay_surface.get_width() * 83/100, 230))) #$250
        self.context.surface_loader.shop_surface.blit(self.context.text_renderer.shop_legendary_price_text, self.context.text_renderer.shop_legendary_price_text.get_rect(center=(self.context.screen.display_surface.get_width() * self.underlay_position + self.context.surface_loader.shop_underlay_surface.get_width() * 83/100, 230))) #$500
        #collection counts
        self.context.surface_loader.shop_surface.blit(self.context.text_renderer.shop_common_collection_text, self.context.text_renderer.shop_common_collection_text.get_rect(center=(self.context.screen.display_surface.get_width() * self.underlay_position + self.context.surface_loader.shop_underlay_surface.get_width() * 83/100, 230))) #$500
        self.context.surface_loader.shop_surface.blit(self.context.text_renderer.shop_uncommon_collection_text, self.context.text_renderer.shop_uncommon_collection_text.get_rect(center=(self.context.screen.display_surface.get_width() * self.underlay_position + self.context.surface_loader.shop_underlay_surface.get_width() * 83/100, 230))) #$500
        self.context.surface_loader.shop_surface.blit(self.context.text_renderer.shop_rare_collection_text, self.context.text_renderer.shop_rare_collection_text.get_rect(center=(self.context.screen.display_surface.get_width() * self.underlay_position + self.context.surface_loader.shop_underlay_surface.get_width() * 83/100, 230))) #$500
        self.context.surface_loader.shop_surface.blit(self.context.text_renderer.shop_legendary_collection_text, self.context.text_renderer.shop_legendary_collection_text.get_rect(center=(self.context.screen.display_surface.get_width() * self.underlay_position + self.context.surface_loader.shop_underlay_surface.get_width() * 83/100, 230))) #$500

