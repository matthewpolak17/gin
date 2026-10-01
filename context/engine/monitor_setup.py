from screeninfo import get_monitors
import os

class Monitor:
    def __init__(self, context):
        self.context = context
        monitors = get_monitors()
        display_monitor = monitors[0]
        #os.environ['SDL_VIDEO_WINDOW_POS'] = f"{display_monitor.x},{display_monitor.y}"
        self.native_height = display_monitor.height
        self.native_width = display_monitor.width
