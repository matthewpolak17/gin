import pygame

class Drawer:
    def __init__(self, context):
        self.context = context
        self.counter = 0
    
    def draw_loading_frame(self, frame, surface):
        surface.blit(frame, (self.context.screen.display_width - 2*frame.get_width() ,self.context.screen.display_height - 2*frame.get_height()))

    def draw_menu(self, surface, menu_active, dt):
        if menu_active:
            self.context.screen.hamburger_x = max(self.context.screen.hamburger_x - (self.context.constants.MENU_SPEED * dt), -1.5 * self.context.constants.HAMBURGER_WIDTH) 
            self.context.screen.menu_x = min(self.context.screen.menu_x + (self.context.constants.MENU_SPEED * dt), 0)
            self.context.rects.update_option_rects()
            surface.blit(self.context.surface_loader.side_overlay, (self.context.screen.menu_x, 0))
            surface.blit(self.context.text_renderer.r_option_text, self.context.text_renderer.r_option_text.get_rect(center=self.context.rects.r_option_rect.center)) #retry option
            surface.blit(self.context.text_renderer.mm_option_text, self.context.text_renderer.mm_option_text.get_rect(center=self.context.rects.mm_option_rect.center)) #main menu option
            surface.blit(self.context.text_renderer.c_option_text, self.context.text_renderer.c_option_text.get_rect(center=self.context.rects.c_option_rect.center)) #customize option
            surface.blit(self.context.text_renderer.s_option_text, self.context.text_renderer.s_option_text.get_rect(center=self.context.rects.s_option_rect.center)) #settings option
            surface.blit(self.context.text_renderer.qg_option_text, self.context.text_renderer.qg_option_text.get_rect(center=self.context.rects.qg_option_rect.center)) #quit game option
        else: 
            surface.blit(self.context.surface_loader.side_overlay, (self.context.screen.menu_x, 0))
            self.context.screen.hamburger_x = min(self.context.screen.hamburger_x + (self.context.constants.MENU_SPEED * dt), 30)
            self.context.screen.menu_x = max(self.context.screen.menu_x - (self.context.constants.MENU_SPEED * dt), -1.5 * self.context.screen.menu_width)
            self.context.rects.update_option_rects()
            surface.blit(self.context.text_renderer.r_option_text, self.context.text_renderer.r_option_text.get_rect(center=self.context.rects.r_option_rect.center)) #retry option
            surface.blit(self.context.text_renderer.mm_option_text, self.context.text_renderer.mm_option_text.get_rect(center=self.context.rects.mm_option_rect.center)) #main menu option
            surface.blit(self.context.text_renderer.c_option_text, self.context.text_renderer.c_option_text.get_rect(center=self.context.rects.c_option_rect.center)) #customize option
            surface.blit(self.context.text_renderer.s_option_text, self.context.text_renderer.s_option_text.get_rect(center=self.context.rects.s_option_rect.center)) #settings option
            surface.blit(self.context.text_renderer.qg_option_text, self.context.text_renderer.qg_option_text.get_rect(center=self.context.rects.qg_option_rect.center)) #quit game option

        #menu icon
        pygame.draw.rect(surface, "white", pygame.Rect(self.context.screen.hamburger_x,30,self.context.constants.HAMBURGER_WIDTH,8))
        pygame.draw.rect(surface, "white", pygame.Rect(self.context.screen.hamburger_x,45,self.context.constants.HAMBURGER_WIDTH,8))
        pygame.draw.rect(surface, "white", pygame.Rect(self.context.screen.hamburger_x,60,self.context.constants.HAMBURGER_WIDTH,8))

    def draw_title_wipe_frame(self, frame, surface):
        surface.blit(self.context.surface_loader.game_surface, (0, 0), area=pygame.Rect(0, 0, frame, self.context.screen.display_height))

    def draw_title_background(self):
        frame = self.context.animator.title_background.frame
        self.context.surface_loader.title_surface.blit(self.context.image_loader.title_background, (-frame, 0))
        self.context.surface_loader.title_surface.blit(self.context.image_loader.title_background, (-frame + self.context.image_loader.title_background_width, 0))  
        self.context.surface_loader.title_surface.blit(self.context.text_renderer.start_text, self.context.rects.start_rect)
        self.context.surface_loader.title_surface.blit(self.context.text_renderer.multiplayer_text, self.context.rects.multiplayer_rect)
    
    def draw_title_text(self):
        surface = self.context.text_renderer.title_text
        x = (self.context.screen.display_width - surface.get_width()) // 2
        y = (self.context.screen.display_height - surface.get_height()) * 5/12
        self.context.surface_loader.title_surface.blit(surface, (x, y))

# ==========================================
# GAME SURFACE METHODS
# ==========================================

    def draw_button(self, rect, text_surface, visible=True):
        if not visible:
            return
        pygame.draw.rect(self.context.surface_loader.game_surface, (200, 200, 200), rect, border_radius=8)
        pygame.draw.rect(self.context.surface_loader.game_surface, self.context.constants.BLACK, rect, 2, border_radius=8)
        text_rect = text_surface.get_rect(center=rect.center)
        self.context.surface_loader.game_surface.blit(text_surface, text_rect)

    def draw_buttons(self):
        self.draw_button(
            self.context.rects.sort_rect_rank,
            self.context.text_renderer.sort_rank_text
        )

        self.draw_button(
            self.context.rects.sort_rect_suit,
            self.context.text_renderer.sort_suit_text
        )

        self.draw_button(
            self.context.rects.player_knock_rect,
            self.context.text_renderer.player_knock_text,
            visible=self.context.hand.can_knock
        )

        self.draw_button(
            self.context.rects.opp_knock_rect,
            self.context.text_renderer.opp_knock_text,
            visible=self.context.opp_hand.can_knock
        )

    def draw_game_background(self):
        self.context.surface_loader.game_surface.blit(self.context.image_loader.background, (0,0))

    def draw_cards(self):
        surface = self.context.surface_loader.game_surface
        surface.blit(self.context.image_loader.blue_back, (surface.get_width() * 4/9 - self.context.constants.CARD_WIDTH / 2, surface.get_height() / 2 - self.context.constants.CARD_HEIGHT / 2))
        pygame.draw.rect(surface, "white", pygame.Rect(surface.get_width() * 5/9 - self.context.constants.CARD_WIDTH / 2, surface.get_height() / 2 - self.context.constants.CARD_HEIGHT / 2, 73, 98), 4, border_radius=10)

        if self.context.discard_pile.cards:
            if len(self.context.discard_pile.cards) > 1:
                second_card = self.context.discard_pile.cards[-2]
                if second_card.visible:
                    discard_top = self.context.image_loader.card_images[second_card.name]
                    surface.blit(discard_top, (surface.get_width() * 5/9 - self.context.constants.CARD_WIDTH / 2, surface.get_height() / 2 - self.context.constants.CARD_HEIGHT / 2))
            if self.context.discard_pile.cards[-1].visible:
                discard_top = self.context.image_loader.card_images[self.context.discard_pile.cards[-1].name]
                surface.blit(discard_top, (surface.get_width() * 5/9 - self.context.constants.CARD_WIDTH / 2, surface.get_height() / 2 - self.context.constants.CARD_HEIGHT / 2))

    def draw_hand_cards(self, active_card, drawn_card):
        surface = self.context.surface_loader.game_surface
        if not active_card:
            for card in self.context.hand.cards:
                if card is drawn_card:
                    continue
                if card.visible:
                    surface.blit(self.context.image_loader.card_images[card.name], card.loc)
        else:
            active_card_x = active_card.loc[0]
            for card in self.context.hand.cards:
                if card.loc[0] < active_card_x and card is not drawn_card and card.visible: #draw all the card before the active card first
                    surface.blit(self.context.image_loader.card_images[card.name], (card.loc))

            temp_image = self.context.image_loader.card_images[active_card.name].copy()
            temp_image.set_alpha(200)
            surface.blit(temp_image, (active_card.loc)) #draw the active card

            for card in self.context.hand.cards:
                if card.loc[0] > active_card_x and card is not drawn_card and card.visible: #draw all the cards after the active card last
                    surface.blit(self.context.image_loader.card_images[card.name], (card.loc))

    def draw_player_card_flip(self, drawn_card, start_pos, end_pos):
        progress = self.context.animator.player_card_flip.get_progress()
        progress_eased = 1 - (1 - progress) ** 3
        x = start_pos[0] + (end_pos[0] - start_pos[0]) * progress_eased
        y = start_pos[1] + (end_pos[1] - start_pos[1]) * progress_eased
        if progress < 0.5:
            scale = 1 - (2 * progress)
            image = self.context.image_loader.blue_back
        else:
            scale = (2 * progress) - 1
            image = self.context.image_loader.card_images[drawn_card.name]
        
        scaled_width = max(1, int(image.get_width() * scale))
        scaled_image = pygame.transform.scale(image, (scaled_width, image.get_height()))

        draw_x = int(x - scaled_width // 2)
        draw_y = int(y - image.get_height() // 2)
        self.context.surface_loader.game_surface.blit(scaled_image, (draw_x, draw_y))
        
    def draw_player_card_slide(self, drawn_card, start_pos, end_pos):
        progress = self.context.animator.player_card_slide.get_progress()
        progress_eased = progress_eased = 1 - (1 - progress) ** 3
        x = start_pos[0] + (end_pos[0] - start_pos[0]) * progress_eased #moves closer to the end_pos using the difference
        y = start_pos[1] + (end_pos[1] - start_pos[1]) * progress_eased
        self.context.surface_loader.game_surface.blit(self.context.image_loader.card_images[drawn_card.name], (x,y))

# ==========================================
# OPP HAND DRAW METHODS                 
# ==========================================

    def draw_opp_hand_cards(self, discard_top, opp_drawn_card, simulated_opp_hand_prepickup, simulated_opp_hand_pickup, opp_discarded_card, simulated_opp_hand_discard):
        surface = self.context.surface_loader.game_surface
        opp_flip_active = self.context.animator.opp_card_flip.active
        opp_slide_active = self.context.animator.opp_card_slide.active
        pickup_shift_progress = self.context.animator.opp_hand_shift_pickup.get_progress()
        pickup_shift_progress = 1 - (1 - pickup_shift_progress) ** 3

        discard_shift_progress = self.context.animator.opp_hand_shift_discard.get_progress()
        discard_shift_progress = 1 - (1 - discard_shift_progress) ** 3

        #opp hand pickup animation
        if (opp_flip_active or opp_slide_active) and self.context.animator.opp_hand_shift_pickup.active:
            suppressed_index = next(i for i, (card, loc) in enumerate(simulated_opp_hand_pickup) if card is opp_drawn_card)
            suppressed_loc = next(loc for c, loc in simulated_opp_hand_pickup if c is opp_drawn_card)

            i = 0
            for card, old_loc in simulated_opp_hand_prepickup:
                new_loc = next(loc for c, loc in simulated_opp_hand_pickup if c is card)

                if i == suppressed_index:
                    if opp_flip_active:
                        self.draw_opp_card_flip(discard_top, self.context.rects.discard_rect.center, (suppressed_loc[0] + 73/2, suppressed_loc[1] + 98/2))
                    else:
                         self.draw_opp_card_slide(self.context.rects.draw_rect, (suppressed_loc[0], suppressed_loc[1]))

                #surface.blit(self.context.image_loader.card_images[card.name], (old_loc[0] + ((new_loc[0] - old_loc[0]) * pickup_shift_progress), card.loc[1])) #uncomment for testing
                surface.blit(self.context.image_loader.blue_back, (old_loc[0] + (new_loc[0] - old_loc[0]) * pickup_shift_progress, card.loc[1]))    
                i += 1

            if suppressed_index >= len(simulated_opp_hand_prepickup):
                if opp_flip_active:
                    self.draw_opp_card_flip(discard_top, self.context.rects.discard_rect.center, (suppressed_loc[0] + 73/2, suppressed_loc[1] + 98/2))
                else:
                    self.draw_opp_card_slide(self.context.rects.draw_rect, suppressed_loc)

        #opp hand discard animation
        elif self.context.animator.opp_discard_flip.active and self.context.animator.opp_card_flip.finished and self.context.animator.opp_card_slide.finished and self.context.animator.opp_hand_shift_pickup.finished:
            suppressed_index = next(i for i, (card, loc) in enumerate(simulated_opp_hand_pickup) if card is opp_discarded_card)
            suppressed_loc = next(loc for c, loc in simulated_opp_hand_pickup if c is opp_discarded_card)
            
            i = 0
            for card, old_loc in simulated_opp_hand_discard:
                new_loc = next(loc for c, loc in simulated_opp_hand_discard if c is card)

                if i == suppressed_index:
                    self.draw_opp_discard_flip((suppressed_loc[0] + 73/2, suppressed_loc[1] + 98/2), self.context.rects.discard_rect.center)
                
                #surface.blit(self.context.image_loader.card_images[card.name], (old_loc[0] + ((new_loc[0] - old_loc[0]) * discard_shift_progress), card.loc[1])) #uncomment for testing
                surface.blit(self.context.image_loader.blue_back, (old_loc[0] + (new_loc[0] - old_loc[0]) * discard_shift_progress, card.loc[1]))  
                i += 1  

            if suppressed_index >= len(simulated_opp_hand_discard):
                self.draw_opp_discard_flip((suppressed_loc[0] + 73/2, suppressed_loc[1] + 98/2), self.context.rects.discard_rect.center)

        else:
            for card in self.context.opp_hand.cards:
                if card.visible:
                    #surface.blit(self.context.image_loader.card_images[card.name], card.loc) #uncomment for testing
                    surface.blit(self.context.image_loader.blue_back, card.loc)

    def draw_opp_card_slide(self, start_pos, end_pos):
        progress = self.context.animator.opp_card_slide.get_progress()
        progress_eased = progress_eased = 1 - (1 - progress) ** 3
        x = start_pos[0] + (end_pos[0] - start_pos[0]) * progress_eased #moves closer to the end_pos using the difference
        y = start_pos[1] + (end_pos[1] - start_pos[1]) * progress_eased
        self.context.surface_loader.game_surface.blit(self.context.image_loader.blue_back, (x,y))

    def draw_opp_card_flip(self, discard_top, start_pos, end_pos):
        progress = self.context.animator.opp_card_flip.get_progress()
        progress_eased = progress_eased = 1 - (1 - progress) ** 3
        x = start_pos[0] + (end_pos[0] - start_pos[0]) * progress_eased
        y = start_pos[1] + (end_pos[1] - start_pos[1]) * progress_eased
        if progress < 0.5:
            scale = 1 - (2 * progress)
            image = self.context.image_loader.card_images[discard_top.name]
        else:
            scale = (2 * progress) - 1
            image = self.context.image_loader.blue_back
        
        scaled_width = max(1, int(image.get_width() * scale))
        scaled_image = pygame.transform.scale(image, (scaled_width, image.get_height()))

        draw_x = int(x - scaled_width // 2)
        draw_y = int(y - image.get_height() // 2)
        self.context.surface_loader.game_surface.blit(scaled_image, (draw_x, draw_y))
    
    def draw_opp_discard_flip(self, start_pos, end_pos):
        progress = self.context.animator.opp_discard_flip.get_progress()
        progress_eased = progress_eased = 1 - (1 - progress) ** 3
        x = start_pos[0] + (end_pos[0] - start_pos[0]) * progress_eased
        y = start_pos[1] + (end_pos[1] - start_pos[1]) * progress_eased
        if progress < 0.5:
            scale = 1 - (2 * progress)
            image = self.context.image_loader.blue_back
        else:
            scale = (2 * progress) - 1
            image = self.context.image_loader.card_images[self.context.discard_pile.cards[-1].name]
        
        scaled_width = max(1, int(image.get_width() * scale))
        scaled_image = pygame.transform.scale(image, (scaled_width, image.get_height()))

        draw_x = int(x - scaled_width // 2)
        draw_y = int(y - image.get_height() // 2)
        self.context.surface_loader.game_surface.blit(scaled_image, (draw_x, draw_y))

    def draw_round_overlay(self, round_overlay):
        if round_overlay:
            self.context.surface_loader.game_surface.blit(self.context.surface_loader.overlay_surface, (0,0))
            #if self.context.text_renderer.player_score_text and self.context.text_renderer.opp_score_text:
            self.context.screen.game_surface.blit(self.context.text_renderer.continue_text, self.context.text_renderer.continue_text.get_rect(center=(self.context.screen.display_width // 2, self.context.screen.display_height * 2/3)))
            self.context.screen.game_surface.blit(self.context.text_renderer.player_score_text, self.context.text_renderer.player_score_text.get_rect(center=(self.context.screen.display_width // 2, self.context.screen.display_height * 1/3)))
            self.context.screen.game_surface.blit(self.context.text_renderer.opp_score_text, self.context.text_renderer.opp_score_text.get_rect(center=(self.context.screen.display_width // 2, (self.context.screen.display_height * 1/3) + 25)))

