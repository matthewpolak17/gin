from context.engine import constants
import pygame

class Rects:
    def __init__(self, screen, text_renderer):
        self.screen = screen
        self.text_renderer = text_renderer

        self.menu_rect = pygame.Rect(20,20,70,58)
        self.start_rect = text_renderer.start_text.get_rect(center=(screen.display_width // 2, screen.display_height // 2))
        self.multiplayer_rect = text_renderer.multiplayer_text.get_rect(center=(screen.display_width // 2, screen.display_height // 1.85))
        self.multiplayer_menu_rect = text_renderer.multiplayer_menu_text.get_rect(center=(screen.display_width // 2, screen.display_height // 2))
        self.main_menu_overlay_rect = pygame.Rect(self.screen.menu_width, 0, self.screen.display_surface.get_width() - self.screen.menu_width, self.screen.display_height)
        self.sort_rect_rank = pygame.Rect(self.screen.display_width * 2/3, self.screen.display_height * 0.75, 80, 40)
        self.sort_rect_suit = pygame.Rect(self.screen.display_width * 2/3, self.screen.display_height * 0.8, 80, 40)
        self.player_knock_rect = pygame.Rect(self.screen.display_width * 2/3, self.screen.display_height * 0.7, 80, 40)
        self.opp_knock_rect = pygame.Rect(self.screen.display_surface.get_width() - 60, self.screen.display_surface.get_height() - 90, 30, 10)
        self.draw_rect = pygame.Rect(self.screen.display_surface.get_width() * 4/9 - constants.CARD_WIDTH / 2, self.screen.display_surface.get_height() / 2 - constants.CARD_HEIGHT / 2, constants.CARD_WIDTH, constants.CARD_HEIGHT)
        self.discard_rect = pygame.Rect(self.screen.display_surface.get_width() * 5/9 - constants.CARD_WIDTH / 2, self.screen.display_surface.get_height() / 2 - constants.CARD_HEIGHT / 2, constants.CARD_WIDTH, constants.CARD_HEIGHT)
        self.update_option_rects()

    def update_option_rects(self):
        self.screen.update_option_locations()
        self.r_option_rect = pygame.Rect(self.screen.option_left, self.screen.option_top, self.screen.option_width, self.screen.option_height) #retry option
        self.mm_option_rect = pygame.Rect(self.screen.option_left, self.screen.option_top*2, self.screen.option_width, self.screen.option_height) #main menu option
        self.c_option_rect = pygame.Rect(self.screen.option_left, self.screen.option_top*3, self.screen.option_width, self.screen.option_height) #customize option
        self.s_option_rect = pygame.Rect(self.screen.option_left, self.screen.option_top*4, self.screen.option_width, self.screen.option_height) #settings option
        self.qg_option_rect = pygame.Rect(self.screen.option_left, self.screen.option_top*5, self.screen.option_width, self.screen.option_height) #quit game option
