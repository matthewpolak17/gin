from context.engine.animation import Animation
import pygame

class Animator:
    def __init__(self, context):
        self.context = context
        self.frame = 0
        self.frame_timer = 0
        self.loading = Animation(0.05, 11)
        self.title_wipe = Animation(0.05, self.context.screen.display_width)
        self.title_background = Animation(0.01, self.context.screen.display_width, True, True)
        self.title_text = Animation(0.005, 40, False)
        self.player_card_flip = Animation((1/self.context.constants.CARD_MOVEMENT_SPEED), 90, False)
        self.player_card_slide = Animation((1/self.context.constants.CARD_MOVEMENT_SPEED), 90, False)
        self.opp_card_flip = Animation((1/self.context.constants.CARD_MOVEMENT_SPEED), 90, False)
        self.opp_card_slide = Animation((1/self.context.constants.CARD_MOVEMENT_SPEED), 90, False)
        self.opp_discard_flip = Animation((1/self.context.constants.CARD_MOVEMENT_SPEED), 90, False)
        self.opp_hand_shift_pickup = Animation(0.01, 50, False)
        self.opp_hand_shift_discard = Animation(0.01, 50, False)

    def opp_hand_pickup_shift(self):
        if self.opp_hand_pickup_shift.active:
            self.opp_hand_pickup_shift.update(self.context.dt)

    def animate_loading(self, dt, surface):
        self.loading.update(dt)
        self.context.drawer.draw_loading_frame(self.context.image_loader.loading_frames[self.frame], surface)

    def animate_title_wipe(self, dt, surface):
        self.title_wipe.update(dt)
        self.context.drawer.draw_title_wipe_frame(self.title_wipe.frame, surface)
        self.title_wipe.mark_finished()

    def animate_title_background(self):
        self.title_background.update(self.context.dt)
    
    def animate_title_text(self):
        if self.title_text.active:
            self.title_text.update(self.context.dt)
            progress = self.title_text.frame / self.title_text.total_frames
            current_font_size = int(140 + 40 * progress)
            self.context.ui_text.title_font = pygame.font.Font(r'assets\fonts\Mermaid1001.ttf', current_font_size)
            
            alpha = int(255 * (1-progress) ** 2) # compute alpha first
            new_surface = self.context.ui_text.render_title("Gin Rummy", self.context.constants.TAN)
            new_surface.set_alpha(alpha)
            self.context.text_renderer.title_text = new_surface

    def animate_player_card_flip(self):
        if self.player_card_flip.active:
            self.player_card_flip.update(self.context.dt)

    def animate_player_card_slide(self):
        if self.player_card_slide.active:
            self.player_card_slide.update(self.context.dt)

    def animate_opp_card_flip(self):
        if self.opp_card_flip.active:
            self.opp_card_flip.update(self.context.dt)

    def animate_opp_card_slide(self):
        if self.opp_card_slide.active:
            self.opp_card_slide.update(self.context.dt)

    def animate_opp_discard_flip(self):
        if self.opp_discard_flip.active and not self.opp_card_flip.active and not self.opp_card_slide.active:
            self.opp_discard_flip.update(self.context.dt)

    def animate_opp_hand_shift_pickup(self):
        if self.opp_hand_shift_pickup.active:
            self.opp_hand_shift_pickup.update(self.context.dt)

    def animate_opp_hand_shift_discard(self):
        if self.opp_hand_shift_discard.active and not self.opp_card_flip.active and not self.opp_card_slide.active:
            self.opp_hand_shift_discard.update(self.context.dt)




