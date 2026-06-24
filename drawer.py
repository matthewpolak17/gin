from assets.loaders.surface_loader import SurfaceLoader
from assets.loaders.image_loader import ImageLoader
from ui_elements.rects import Rects
from ui_elements.text_renderer import TextRenderer
import constants
import pygame

class Drawer:
    def __init__(self, screen):
        self.screen = screen
        self.text_renderer = TextRenderer()
        self.image_loader = ImageLoader(self.screen)
        self.surface_loader = SurfaceLoader(self.screen)
        self.rects = Rects(self.screen, self.text_renderer)
    
    def draw_loading_frame(self, frame, surface):
        surface.blit(frame, (self.screen.display_width - 2*frame.get_width() ,self.screen.display_height - 2*frame.get_height()))

    def draw_menu(self, surface, menu_active, dt):
        if menu_active:
            self.screen.hamburger_x = max(self.screen.hamburger_x - (constants.MENU_SPEED * dt), -1.5 * constants.HAMBURGER_WIDTH) 
            self.screen.menu_x = min(self.screen.menu_x + (constants.MENU_SPEED * dt), 0)
            self.rects.update_option_rects()
            surface.blit(self.surface_loader.side_overlay, (self.screen.menu_x, 0))
            surface.blit(self.text_renderer.r_option_text, self.text_renderer.r_option_text.get_rect(center=self.rects.r_option_rect.center)) #retry option
            surface.blit(self.text_renderer.mm_option_text, self.text_renderer.mm_option_text.get_rect(center=self.rects.mm_option_rect.center)) #main menu option
            surface.blit(self.text_renderer.c_option_text, self.text_renderer.c_option_text.get_rect(center=self.rects.c_option_rect.center)) #customize option
            surface.blit(self.text_renderer.s_option_text, self.text_renderer.s_option_text.get_rect(center=self.rects.s_option_rect.center)) #settings option
            surface.blit(self.text_renderer.qg_option_text, self.text_renderer.qg_option_text.get_rect(center=self.rects.qg_option_rect.center)) #quit game option
        else: 
            surface.blit(self.surface_loader.side_overlay, (self.screen.menu_x, 0))
            self.screen.hamburger_x = min(self.screen.hamburger_x + (constants.MENU_SPEED * dt), 30)
            self.screen.menu_x = max(self.screen.menu_x - (constants.MENU_SPEED * dt), -1.5 * self.screen.menu_width)
            self.rects.update_option_rects()
            surface.blit(self.text_renderer.r_option_text, self.text_renderer.r_option_text.get_rect(center=self.rects.r_option_rect.center)) #retry option
            surface.blit(self.text_renderer.mm_option_text, self.text_renderer.mm_option_text.get_rect(center=self.rects.mm_option_rect.center)) #main menu option
            surface.blit(self.text_renderer.c_option_text, self.text_renderer.c_option_text.get_rect(center=self.rects.c_option_rect.center)) #customize option
            surface.blit(self.text_renderer.s_option_text, self.text_renderer.s_option_text.get_rect(center=self.rects.s_option_rect.center)) #settings option
            surface.blit(self.text_renderer.qg_option_text, self.text_renderer.qg_option_text.get_rect(center=self.rects.qg_option_rect.center)) #quit game option

        #menu icon
        pygame.draw.rect(surface, "white", pygame.Rect(self.screen.hamburger_x,30,constants.HAMBURGER_WIDTH,8))
        pygame.draw.rect(surface, "white", pygame.Rect(self.screen.hamburger_x,45,constants.HAMBURGER_WIDTH,8))
        pygame.draw.rect(surface, "white", pygame.Rect(self.screen.hamburger_x,60,constants.HAMBURGER_WIDTH,8))

    def draw_title_wipe_frame(self, frame, surface):
        surface.blit(self.surface_loader.game_surface, (0, 0), area=pygame.Rect(0, 0, frame, self.screen.display_height))

    def draw_title_background_frame(self, frame, surface):
        surface.blit(self.image_loader.title_background, (-frame, 0))
        surface.blit(self.image_loader.title_background, (-frame + self.image_loader.title_background_width, 0))  
        surface.blit(self.text_renderer.start_text, self.rects.start_rect)
        surface.blit(self.text_renderer.multiplayer_text, self.rects.multiplayer_rect)


