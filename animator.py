class Animator:
    def __init__(self, drawer):
        self.drawer = drawer
        self.frame = 0
        self.frame_timer = 0

    def animate_loading(self, dt, surface):

        self.frame_timer += dt

        if self.frame < 11:
            if self.frame_timer >= 0.05:
                self.frame_timer = 0
                self.frame += 1
        else:
            self.frame = 0

        frames = {
            0: self.drawer.image_loader.loading_frame_0,
            1: self.drawer.image_loader.loading_frame_1,
            2: self.drawer.image_loader.loading_frame_2,
            3: self.drawer.image_loader.loading_frame_3,
            4: self.drawer.image_loader.loading_frame_4,
            5: self.drawer.image_loader.loading_frame_5,
            6: self.drawer.image_loader.loading_frame_6,
            7: self.drawer.image_loader.loading_frame_7,
            8: self.drawer.image_loader.loading_frame_8,
            9: self.drawer.image_loader.loading_frame_9,
            10: self.drawer.image_loader.loading_frame_10,
            11: self.drawer.image_loader.loading_frame_11
        }
       
        self.drawer.draw_loading_frame(frames[self.frame], surface)


