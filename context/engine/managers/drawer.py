import pygame

class Drawer:
    def __init__(self, context):
        self.context = context
    
    @property
    def menu_rect(self):
        return self.context.rects.menu_rect
    
    @property
    def main_menu_overlay_rect(self):
        return self.context.rects.main_menu_overlay_rect
    
    @property
    def draw_rect(self):
        return self.context.rects.draw_rect
    
    def draw_to_game_surface(self, image, x, y):
        self.context.surface_loader.game_surface.blit(image, (x,y))
    
    def draw_loading_frame(self, frame, surface):
        surface.blit(frame, (self.context.screen.display_width - 2*frame.get_width() ,self.context.screen.display_height - 2*frame.get_height()))

    def draw_menu(self, surface, menu_active, dt):
        if menu_active:
            self.context.screen.hamburger_x = max(self.context.screen.hamburger_x - (self.context.constants.MENU_SPEED * dt), -1.5 * self.context.constants.HAMBURGER_WIDTH) 
            self.context.screen.menu_x = min(self.context.screen.menu_x + (self.context.constants.MENU_SPEED * dt), 0)
            self.context.rects.update_option_rects()
            surface.blit(self.context.surface_loader.side_overlay, (self.context.screen.menu_x, 0))
            surface.blit(self.context.text_renderer.r_option_text, self.context.text_renderer.r_option_text.get_rect(center=self.context.rects.r_option_rect.center)) #retry option
            surface.blit(self.context.text_renderer.mm_option_text, self.context.text_renderer.mm_option_text.get_rect(center=self.context.rects.mm_option_rect.center)) #main menu option
            surface.blit(self.context.text_renderer.c_option_text, self.context.text_renderer.c_option_text.get_rect(center=self.context.rects.c_option_rect.center)) #customize option
            surface.blit(self.context.text_renderer.s_option_text, self.context.text_renderer.s_option_text.get_rect(center=self.context.rects.s_option_rect.center)) #settings option
            surface.blit(self.context.text_renderer.qg_option_text, self.context.text_renderer.qg_option_text.get_rect(center=self.context.rects.qg_option_rect.center)) #quit game option
        else: 
            surface.blit(self.context.surface_loader.side_overlay, (self.context.screen.menu_x, 0))
            self.context.screen.hamburger_x = min(self.context.screen.hamburger_x + (self.context.constants.MENU_SPEED * dt), 30)
            self.context.screen.menu_x = max(self.context.screen.menu_x - (self.context.constants.MENU_SPEED * dt), -1.5 * self.context.screen.menu_width)
            self.context.rects.update_option_rects()
            surface.blit(self.context.text_renderer.r_option_text, self.context.text_renderer.r_option_text.get_rect(center=self.context.rects.r_option_rect.center)) #retry option
            surface.blit(self.context.text_renderer.mm_option_text, self.context.text_renderer.mm_option_text.get_rect(center=self.context.rects.mm_option_rect.center)) #main menu option
            surface.blit(self.context.text_renderer.c_option_text, self.context.text_renderer.c_option_text.get_rect(center=self.context.rects.c_option_rect.center)) #customize option
            surface.blit(self.context.text_renderer.s_option_text, self.context.text_renderer.s_option_text.get_rect(center=self.context.rects.s_option_rect.center)) #settings option
            surface.blit(self.context.text_renderer.qg_option_text, self.context.text_renderer.qg_option_text.get_rect(center=self.context.rects.qg_option_rect.center)) #quit game option

        #menu icon
        pygame.draw.rect(surface, "white", pygame.Rect(self.context.screen.hamburger_x,30,self.context.constants.HAMBURGER_WIDTH,8))
        pygame.draw.rect(surface, "white", pygame.Rect(self.context.screen.hamburger_x,45,self.context.constants.HAMBURGER_WIDTH,8))
        pygame.draw.rect(surface, "white", pygame.Rect(self.context.screen.hamburger_x,60,self.context.constants.HAMBURGER_WIDTH,8))

    def draw_title_wipe_frame(self, frame, surface):
        surface.blit(self.context.surface_loader.game_surface, (0, 0), area=pygame.Rect(0, 0, frame, self.context.screen.display_height))

    def draw_title_background_frame(self, frame, surface):
        surface.blit(self.context.image_loader.title_background, (-frame, 0))
        surface.blit(self.context.image_loader.title_background, (-frame + self.context.image_loader.title_background_width, 0))  
        surface.blit(self.context.text_renderer.start_text, self.context.rects.start_rect)
        surface.blit(self.context.text_renderer.multiplayer_text, self.context.rects.multiplayer_rect)
    
    def draw_button(self, rect, text_surface, visible=True):
        if not visible:
            return
        pygame.draw.rect(self.context.surface_loader.game_surface, (200, 200, 200), rect, border_radius=8)
        pygame.draw.rect(self.context.surface_loader.game_surface, self.context.constants.BLACK, rect, 2, border_radius=8)
        text_rect = text_surface.get_rect(center=rect.center)
        self.context.surface_loader.game_surface.blit(text_surface, text_rect)

    def draw_buttons(self):
        self.draw_button(
            self.context.drawer.rects.sort_rect_rank,
            self.context.drawer.text_renderer.sort_rank_text
        )

        self.draw_button(
            self.context.drawer.rects.sort_rect_suit,
            self.context.drawer.text_renderer.sort_suit_text
        )

        self.draw_button(
            self.context.drawer.rects.player_knock_rect,
            self.context.drawer.text_renderer.player_knock_text,
            visible=self.context.hand.can_knock
        )

        self.draw_button(
            self.context.drawer.rects.opp_knock_rect,
            self.context.drawer.text_renderer.opp_knock_text,
            visible=self.context.opp_hand.can_knock
        )

    
