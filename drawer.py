from assets.loaders.surface_loader import SurfaceLoader
from assets.loaders.image_loader import ImageLoader
from ui_elements.rects import Rects
from ui_elements.text_renderer import TextRenderer

class Drawer:
    def __init__(self, screen):
        self.text_renderer = TextRenderer()
        self.image_loader = ImageLoader(screen)
        self.surface_loader = SurfaceLoader(screen)
        self.rects = Rects(screen, self.text_renderer)
    
    def draw_loading_frame(self, frame, surface):

        surface.blit(frame, (900,300)) #static




