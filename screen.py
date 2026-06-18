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