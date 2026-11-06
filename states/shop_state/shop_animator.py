from context.engine.animation import Animation
import pygame

class ShopAnimator:
    def __init__(self, context):
        self.context = context
        self.frame = 0
        self.frame_timer = 0 
        self.coin = Animation(0.02, 19, True, True)

    def animate_coin(self):
        self.coin.update(self.context.dt)


