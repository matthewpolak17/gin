import pygame
from monitor_setup import Monitor

class Screen:
    def __init__(self):
        pygame.display.set_caption("Gin Rummy")

        monitor = Monitor()
        flags = pygame.NOFRAME | pygame.HWSURFACE | pygame.DOUBLEBUF
        self.display_surface = pygame.display.set_mode((monitor.native_width, monitor.native_height), flags)
        self.display_width = monitor.native_width
        self.display_height = monitor.native_height

        #menu dimensions
        self.menu_width = self.display_surface.get_width() / 8
        self.menu_x = -1.5 * self.menu_width
        self.hamburger_x = 30 #not dependent on screen at the moment, but it probably should be in the future
        
        #menu options
        self.update_option_locations()
    
    def update_option_locations(self):
        self.option_width = self.display_width / 10
        self.option_height = self.display_height / 15
        self.option_left = self.menu_x + self.menu_width / 2 - self.option_width / 2
        self.option_top = self.display_height / 11
