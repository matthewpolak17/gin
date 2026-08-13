import pygame
import math

class TitleDrawer:
    def __init__(self, context):
        self.context = context
        self.counter = 0
    
    def draw_coin_frame(self):
        frame = self.context.image_loader.coin_frames[self.context.title_animator.coin.frame]
        print(self.context.title_animator.coin.frame)
        self.context.surface_loader.title_surface.blit(frame, (self.context.screen.display_width - 2*frame.get_width() ,self.context.screen.display_height - 2*frame.get_height()))