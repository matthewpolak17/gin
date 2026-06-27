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
        self.player_card_flip = Animation(0.05, 40, False)
        self.card_slide = Animation(0.05, 40)
        self.card_hover_y = Animation(0.02, 20, False)

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
            self.context.text_renderer.title_text = new_surface  # assign back!

    def animate_player_card_flip(self):
        if self.player_card_flip.active:
            self.player_card_flip.update(self.context.dt)
    
    def animate_opp_card_flip(self, opp_drawn_card, start_pos, end_pos):
        self.card_flip.update(self.context.dt)
        progress = self.card_flip.frame / self.card_flip.total_frames
        progress_eased = progress_eased = 1 - (1 - progress) ** 3
        x = start_pos[0] + (end_pos[0] - start_pos[0]) * progress_eased
        y = start_pos[1] + (end_pos[1] - start_pos[1]) * progress_eased
        if self.card_flip:
            scale = 1 - (2 * progress - 0.5)
            image = self.context.image_loader.card_images[opp_drawn_card.name]
        else:
            scale = 2 * (progress - 0.5)
            image = self.context.image_loader.blue_back
        
        scaled_width = max(1, int(image.get_width() * scale))
        scaled_image = pygame.transform.scale(image, (scaled_width, image.get_height()))

        draw_x = int(x - scaled_width // 2)
        draw_y = int(y - image.get_height() // 2)
        self.context.drawer.draw_cards()
        self.context.drawer.draw_to_game_surface(scaled_image, draw_x, draw_y)

    def animate_card_slide_move(self, front_img, start_pos, end_pos):
        self.card_slide.update(self.context.dt)
        progress = self.card_slide.frame / self.card_slide.total_frames
        progress_eased = progress_eased = 1 - (1 - progress) ** 3
        x = start_pos[0] + (end_pos[0] - start_pos[0]) * progress_eased #moves closer to the end_pos using the difference
        y = start_pos[1] + (end_pos[1] - start_pos[1]) * progress_eased
        self.context.drawer.draw_to_game_surface(front_img, (x,y))

    def animate_card_hover(self):
        self.card_hover_y.update(self.context.dt)





