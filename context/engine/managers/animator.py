from context.engine.animation import Animation

class Animator:
    def __init__(self, drawer):
        self.drawer = drawer
        self.frame = 0
        self.frame_timer = 0
        self.loading = Animation(0.05, 11)
        self.title_wipe = Animation(0.05, self.drawer.screen.display_width)
        self.title_background = Animation(0.05, self.drawer.screen.display_width)

    def animate_loading(self, dt, surface):
        self.loading.update(dt)
        self.drawer.draw_loading_frame(self.drawer.image_loader.loading_frames[self.frame], surface)

    def animate_title_wipe(self, dt, surface):
        self.title_wipe.update(dt)
        self.drawer.draw_title_wipe_frame(self.title_wipe.frame, surface)
        self.title_wipe.mark_finished()

    def animate_title_background(self, dt, surface):
        self.title_background.update(dt)
        self.drawer.draw_title_background_frame(self.title_background.frame, surface)





