from context.engine.animation import Animation
import pygame

class TitleAnimator:
    def __init__(self, context):
        self.context = context
        self.frame = 0
        self.frame_timer = 0 
        self.coin = Animation(0.04, 19, True, True)
        self.lucky_coin = Animation(0.04, 19, True, True)

    def animate_coin(self):
        self.coin.update(self.context.dt)

    def animate_lucky_coin(self):
        self.lucky_coin.update(self.context.dt)


