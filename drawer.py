from assets.loaders.surface_loader import SurfaceLoader
from assets.loaders.image_loader import ImageLoader
from ui_elements.rects import Rects
from ui_elements.text_renderer import TextRenderer
from screen import Screen

class Drawer:
    def __init__(self):
        self.screen = Screen()
        self.text_renderer = TextRenderer()
        self.image_loader = ImageLoader(self.screen)
        self.surface_loader = SurfaceLoader(self.screen)
        self.rects = Rects(self.screen, self.text_renderer)



