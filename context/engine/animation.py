class Animation:
    def __init__(self, frame_time, total_frames, repeats=True, active=False):
        self.frame_timer = 0        #dt gets added to this
        self.frame_time = frame_time #time between each frame

        self.frame = 0
        self.total_frames = total_frames
        self.active = active
        self.repeats = repeats
        self.finished = False
        

    def update(self, dt):
        if self.finished or not self.active:
            return
        self.frame_timer += dt #advance the timer

        while self.frame_timer >= self.frame_time:
            self.frame_timer -= self.frame_time
            self.frame += 1
            if self.frame >= self.total_frames:
                if self.repeats:
                    self.frame = 0
                else:
                    self.frame = self.total_frames - 1
                    self.finished = True
                    self.active = False
                    break
                
    def start(self):
        self.frame_timer = 0
        self.frame = 0
        self.active = True
        self.finished = False
