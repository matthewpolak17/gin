class Animation:
    def __init__(self, frame_time, total_frames):
        self.frame_timer = 0
        self.frame_time = frame_time #time between each frame

        self.frame = 0
        self.total_frames = total_frames

        self.finished = False
        

    def update(self, dt):
        self.frame_timer += dt #advance the timer

        if self.frame < self.total_frames:  #if the animation hasn't completed yet 
            if self.frame_timer >= self.frame_time: #if the frame_time has been reached
                self.frame_timer = 0                #reset the timer
                self.frame += 1                     #advance to the next frame
        else:
            self.frame = 0

    def mark_finished(self):
        if self.frame >= self.total_frames:
            self.finished = True
