from states.state import State
import pygame

class TitleState(State):
    def __init__(self, manager, context):
        super().__init__(manager)
        self.context = context

    def update(self):
        self.context.animator.animate_title_background()
        self.context.animator.animate_title_text()
        if self.context.animator.title_text.finished:
            self.prepare_wipe()
            self.manager.set("wipe")
    def draw(self):
        self.context.drawer.draw_title_background()
        self.context.drawer.draw_title_text()
        self.context.screen.display_surface.blit(self.context.surface_loader.title_surface, (0,0))

    def exit(self):
        pass

    def enter(self):
        self.context.animator.title_text.reset()
        self.context.ui_text.title_font = pygame.font.Font(r'assets\fonts\Mermaid1001.ttf', 140)
        new_surface = self.context.ui_text.render_title("Gin Rummy", self.context.constants.TAN)
        new_surface.set_alpha(255)
        self.context.text_renderer.title_text = new_surface
        self.context.ui_text

    def handle_event(self, event):

        if event.type == pygame.QUIT:
            self.manager.running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.manager.running = False
            if event.key == pygame.K_RETURN:
                self.context.animator.title_text.start()
            if event.key == pygame.K_LSHIFT:
                self.manager.set("networking")
    
    def prepare_wipe(self):
        #prepares game screen
        self.context.updateLocations()
        self.context.drawer.draw_game_background()
        self.context.drawer.draw_menu(self.context.surface_loader.game_surface, self.manager.menu_active, self.context.dt)
        self.context.drawer.draw_buttons()
        self.context.drawer.draw_hand_cards(None, None)
        self.context.drawer.draw_cards(None, None)

        self.manager.states["wipe"].title_snapshot = self.context.surface_loader.title_surface.copy()
        self.manager.states["wipe"].to_surface = self.context.surface_loader.game_surface.copy()
