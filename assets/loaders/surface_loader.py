import pygame

class SurfaceLoader:
    def __init__(self, screen):
        self.screen = screen
        self.title_surface = pygame.Surface((self.screen.display_width, self.screen.display_height))
        self.game_surface = pygame.Surface((self.screen.display_width, self.screen.display_height))
        self.networking_surface = pygame.Surface((screen.display_width, screen.display_height))
        self.set_side_overlay()
    
    def set_side_overlay(self):
        self.side_overlay = pygame.Surface((self.screen.menu_width, self.screen.display_height), pygame.SRCALPHA)
        self.side_overlay.fill((0,0,0, 80))

