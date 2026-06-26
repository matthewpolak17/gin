import pygame

class SurfaceLoader:
    def __init__(self, context):
        self.context = context
        self.game_surface = pygame.Surface((self.context.screen.display_width, self.context.screen.display_height))
        self.networking_surface = pygame.Surface((self.context.screen.display_width, self.context.screen.display_height))
        self.set_overlay_surface()
        self.set_side_overlay()
    
    def set_side_overlay(self):
        self.side_overlay = pygame.Surface((self.context.screen.menu_width, self.context.screen.display_height), pygame.SRCALPHA)
        self.side_overlay.fill((0,0,0, 80))
    
    def set_overlay_surface(self):
        self.overlay_surface = pygame.Surface(self.context.screen.display_surface.get_size(), pygame.SRCALPHA)
        self.overlay_surface.fill((0,0,0, 120))

