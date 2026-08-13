from states.state import State
import pygame

class NetworkingState(State):
    def __init__(self, manager, context):
        super().__init__(manager)
        self.context = context

    def update(self):
        pass

    def draw(self):
        self.context.surface_loader.networking_surface.blit(self.context.image_loader.networking_background, (0,0))
        self.context.surface_loader.networking_surface.blit(self.context.text_renderer.multiplayer_menu_text, self.context.rects.multiplayer_menu_rect)
        self.context.animator.animate_loading(self.context.dt, self.context.surface_loader.networking_surface)
        self.context.drawer.draw_menu(self.context.surface_loader.networking_surface, self.manager.menu_active, self.context.dt)
        self.context.screen.display_surface.blit(self.context.surface_loader.networking_surface, (0,0))

    def exit(self):
        pass

    def enter(self):
        pass

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.context.rects.menu_rect.collidepoint(event.pos):
                    self.manager.menu_active = True
                if self.context.rects.main_menu_overlay_rect.collidepoint(event.pos):
                    self.manager.menu_active = False
                if self.manager.menu_active:
                    self.context.rects.update_option_rects()
                    if self.context.rects.mm_option_rect.collidepoint(event.pos):
                        self.manager.restart_from_main_menu = True
                    if self.context.rects.qg_option_rect.collidepoint(event.pos):
                        self.manager.running = False
                    if self.context.rects.r_option_rect.collidepoint(event.pos):
                        self.manager.restart = True