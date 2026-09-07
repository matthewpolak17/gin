from states.state import State
from context.engine.animation import Animation
import pygame

class WipeState(State):
    def __init__(self, manager, context):
        super().__init__(manager)
        self.context = context
        self.title_snapshot = None
        self.to_surface = None
        self.wipe = Animation(0.0002, context.screen.display_width, False)
        self.mouse_x, self.mouse_y = (0, 0)

    def enter(self):
        self.wipe.start()

    def update(self):
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        self.context.animator.title_background.update(self.context.dt)
        if self.wipe.active:
            self.wipe.update(self.context.dt)
        if self.wipe.finished:
            self.manager.set("game")

    def draw(self):
        self.context.screen.display_surface.blit(self.to_surface, (0, 0))
        self.context.drawer.draw_title_background()
        clip_width = self.context.screen.display_width - self.wipe.frame
        self.context.screen.display_surface.blit(
            self.context.surface_loader.title_surface, (0, 0),
            area=pygame.Rect(0, 0, clip_width, self.context.screen.display_height)
        )
        self.context.drawer.draw_cursor(self.manager.active_cursor, self.mouse_x, self.mouse_y, self.context.screen.display_surface)