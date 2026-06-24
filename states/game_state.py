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
                    pass