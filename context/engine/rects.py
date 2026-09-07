from context.engine import constants
import pygame

class Rects:
    def __init__(self, context):
        self.context = context

        self.title_rect = self.context.text_renderer.title_text.get_rect(center=(context.screen.display_width / 2, context.screen.display_height * 5/12))
        self.menu_rect = pygame.Rect(20,20,70,58)
        self.start_rect = self.context.text_renderer.start_text.get_rect(center=(self.context.screen.display_width // 2, self.context.screen.display_height // 2))
        self.multiplayer_rect = self.context.text_renderer.multiplayer_text.get_rect(center=(self.context.screen.display_width // 2, self.context.screen.display_height // 1.85))
        self.multiplayer_menu_rect = self.context.text_renderer.multiplayer_menu_text.get_rect(center=(self.context.screen.display_width // 2, self.context.screen.display_height // 2))
        self.main_menu_overlay_rect = pygame.Rect(self.context.screen.menu_width, 0, self.context.screen.display_surface.get_width() - self.context.screen.menu_width, self.context.screen.display_height)
        self.sort_rect_rank = pygame.Rect(self.context.screen.display_width * 2/3, self.context.screen.display_height * 0.75, self.context.image_loader.button.get_width(), self.context.image_loader.button.get_height())
        self.sort_rect_suit = pygame.Rect(self.context.screen.display_width * 2/3, self.context.screen.display_height * 0.8, self.context.image_loader.button.get_width(), self.context.image_loader.button.get_height())
        self.player_knock_rect = pygame.Rect(self.context.screen.display_width * 2/3, self.context.screen.display_height * 0.7, self.context.image_loader.button.get_width(), self.context.image_loader.button.get_height())
        self.draw_rect = pygame.Rect(self.context.screen.display_surface.get_width() * 4/9 - constants.CARD_WIDTH / 2, self.context.screen.display_surface.get_height() / 2 - constants.CARD_HEIGHT / 2, constants.CARD_WIDTH, constants.CARD_HEIGHT)
        self.discard_rect = pygame.Rect(self.context.screen.display_surface.get_width() * 5/9 - constants.CARD_WIDTH / 2, self.context.screen.display_surface.get_height() / 2 - constants.CARD_HEIGHT / 2, constants.CARD_WIDTH, constants.CARD_HEIGHT)
        self.update_option_rects()

    def update_option_rects(self):
        self.context.screen.update_option_locations()
        self.r_option_rect = pygame.Rect(self.context.screen.option_left, self.context.screen.option_top, self.context.screen.option_width, self.context.screen.option_height) #retry option
        self.mm_option_rect = pygame.Rect(self.context.screen.option_left, self.context.screen.option_top*2, self.context.screen.option_width, self.context.screen.option_height) #main menu option
        self.c_option_rect = pygame.Rect(self.context.screen.option_left, self.context.screen.option_top*3, self.context.screen.option_width, self.context.screen.option_height) #customize option
        self.s_option_rect = pygame.Rect(self.context.screen.option_left, self.context.screen.option_top*4, self.context.screen.option_width, self.context.screen.option_height) #settings option
        self.qg_option_rect = pygame.Rect(self.context.screen.option_left, self.context.screen.option_top*5, self.context.screen.option_width, self.context.screen.option_height) #quit game option
