from states.state import State
import pygame

class GameState(State):
    def __init__(self, manager, context):
        super().__init__(manager)
        self.context = context

    def update(self):
        pass
    def draw(self):
        pass
    def exit(self):
        pass
    def enter(self):
        pass
    def handle_event(self, event):
        
        if event.type == pygame.QUIT:
            self.manager.running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.manager.running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.manager.engine.drawer.menu_rect.collidepoint(event.pos):
                    self.manager.menu_active = True
                if self.manager.engine.drawer.main_menu_overlay_rect.collidepoint(event.pos):
                    self.manager.menu_active = False
                if self.manager.menu_active:
                    self.context.drawer.rects.update_option_rects()
                    if self.context.drawer.rects.mm_option_rect.collidepoint(event.pos):
                        self.manager.restart_from_main_menu = True
                    if self.context.drawer.rects.qg_option_rect.collidepoint(event.pos):
                        self.manager.running = False
                    if self.context.drawer.rects.r_option_rect.collidepoint(event.pos):
                        self.manager.restart = True

                for card in reversed(self.context.hand.cards):
                    if card == self.context.hand.cards[-1]:
                        card_rect = pygame.Rect(card.loc[0], card.loc[1], 73, 98)
                    else:
                        card_rect = pygame.Rect(card.loc[0], card.loc[1], ((self.context.screen.display_surface.get_width() / 3) / (len(self.context.hand.cards) - 1)) * 0.8, 98)

                    if card_rect.collidepoint(event.pos):
                        clicked = True
                        active_card = card