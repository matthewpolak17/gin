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
        surface = self.context.surface_loader.shop_surface
        underlay_surface = self.context.surface_loader.shop_underlay_surface
        offset = (self.context.screen.display_surface.get_width() * self.underlay_position, 50)
        rects = self.context.rects
        text = self.context.text_renderer

        surface.blit(text.shop_shop_text, text.shop_shop_text.get_rect(center=(self.context.screen.display_surface.get_width() / 2, 150)))
        surface.blit(text.shop_buy_text, text.shop_buy_text.get_rect(center=(self.context.screen.display_surface.get_width() * self.underlay_position + underlay_surface.get_width() * 20/100, 230)))
        surface.blit(text.shop_collection_text, text.shop_collection_text.get_rect(center=(self.context.screen.display_surface.get_width() * self.underlay_position + underlay_surface.get_width() * 83/100, 230))) 
        
        surface.blit(text.shop_common_text, text.shop_common_text.get_rect(center=(rects.shop_common_rect.move(offset).center))) #common
        surface.blit(text.shop_uncommon_text, text.shop_uncommon_text.get_rect(center=(rects.shop_uncommon_rect.move(offset).center))) #uncommon
        surface.blit(text.shop_rare_text, text.shop_rare_text.get_rect(center=(rects.shop_rare_rect.move(offset).center))) #rare
        surface.blit(text.shop_legendary_text, text.shop_legendary_text.get_rect(center=(rects.shop_legendary_rect.move(offset).center))) #legendary
        
        surface.blit(text.shop_common_price_text, text.shop_common_price_text.get_rect(center=(self.context.screen.display_surface.get_width() * self.underlay_position + underlay_surface.get_width() * 83/100, 230))) #$25
        surface.blit(text.shop_uncommon_price_text, text.shop_uncommon_price_text.get_rect(center=(self.context.screen.display_surface.get_width() * self.underlay_position + underlay_surface.get_width() * 83/100, 230))) #$100
        surface.blit(text.shop_rare_price_text, text.shop_rare_price_text.get_rect(center=(self.context.screen.display_surface.get_width() * self.underlay_position + underlay_surface.get_width() * 83/100, 230))) #$250
        surface.blit(text.shop_legendary_price_text, text.shop_legendary_price_text.get_rect(center=(self.context.screen.display_surface.get_width() * self.underlay_position + underlay_surface.get_width() * 83/100, 230))) #$500
        
        surface.blit(text.shop_common_collection_text, text.shop_common_collection_text.get_rect(center=(self.context.screen.display_surface.get_width() * self.underlay_position + underlay_surface.get_width() * 83/100, 230))) #$500
        surface.blit(text.shop_uncommon_collection_text, text.shop_uncommon_collection_text.get_rect(center=(self.context.screen.display_surface.get_width() * self.underlay_position + underlay_surface.get_width() * 83/100, 230))) #$500
        surface.blit(text.shop_rare_collection_text, text.shop_rare_collection_text.get_rect(center=(self.context.screen.display_surface.get_width() * self.underlay_position + underlay_surface.get_width() * 83/100, 230))) #$500
        surface.blit(text.shop_legendary_collection_text, text.shop_legendary_collection_text.get_rect(center=(self.context.screen.display_surface.get_width() * self.underlay_position + underlay_surface.get_width() * 83/100, 230))) #$500

