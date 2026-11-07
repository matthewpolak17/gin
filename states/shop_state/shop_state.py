from states.state import State
import pygame

class ShopState(State):
    def __init__(self, manager, context):
        super().__init__(manager)
        self.context = context
        self.mouse_x, self.mouse_y = (0, 0)

    def update(self):
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

    def draw(self):
        self.context.shop_drawer.draw_shop_background()
        self.context.shop_drawer.draw_shop_underlay()
        self.context.drawer.draw_menu(self.context.surface_loader.shop_surface, self.manager.menu_active, self.context.dt)
        self.context.shop_drawer.draw_shop_text()
        self.context.drawer.draw_cursor(self.manager.active_cursor, self.mouse_x, self.mouse_y, self.context.surface_loader.shop_surface)
        self.context.screen.display_surface.blit(self.context.surface_loader.shop_surface, (0,0))

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