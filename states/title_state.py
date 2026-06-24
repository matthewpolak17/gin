from states.state import State
import pygame

class TitleState(State):
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
            if event.key == pygame.K_RETURN:
                self.manager.set("game")
            if event.key == pygame.K_LSHIFT:
                self.manager.set("networking")
