from states.state import State
from collections import defaultdict
from itertools import combinations
import random
import pygame

class GameState(State):
    def __init__(self, manager, context):
        super().__init__(manager)
        self.context = context
        self.clicked = False
        self.active_card = None
        self.card_hovered = None
        self.original_loc = (0,0)
        self.original_index = None
        self.turn = 1
        self.card_x = 0
        self.card_y = 0
        self.player_turn = 1
        self.drawn_card = None
        self.discard_top = None
        self.opp_best_discard = None
        self.knocking = False
        self.horizontal_shift = (((self.context.screen.display_surface.get_width() / 3) / len(self.context.hand.cards)) * 0.8)
        self.player_knock = False
        self.computer_knock = False
        self.round_overlay = False

    def update(self):
        self.context.updateLocations() 
        self.update_card_hover()

        self.context.animator.animate_player_card_slide()
        if self.context.animator.player_card_slide.finished:
            self.drawn_card = None
            self.context.hand.cards[-1].visible = True

        self.context.animator.animate_player_card_flip()
        if self.context.animator.player_card_flip.finished:
            self.drawn_card = None
            self.context.hand.cards[-1].visible = True

        self.context.animator.animate_opp_card_slide()
        if self.context.animator.opp_card_slide.finished:
            self.opp_drawn_card = None
        self.context.animator.animate_opp_card_flip()
        if self.context.animator.opp_card_flip.finished:
            self.opp_drawn_card = None
        self.context.animator.animate_opp_discard_flip()

        #hover_x logic
        if self.active_card:
            for i, card in enumerate(self.context.hand.cards):
                if card.dragging:
                    continue
                if card.loc[0] > self.active_card.loc[0] and i < self.original_index and card != self.active_card: #moving active card to the left
                    card.hovered_x = True
                    card.target_x = card.base_x + self.horizontal_shift

                elif card.loc[0] < self.active_card.loc[0] and i > self.original_index and card != self.active_card: #moving active card to the right
                    card.hovered_x = True
                    card.target_x = card.base_x - self.horizontal_shift

                else:
                    card.hovered_x = False
                    card.target_x = card.base_x

                x, y = card.loc
                distance = card.target_x - x
                card.velocity_x += distance * 0.2
                card.velocity_x *= 0.35 #card movement speed
                x += card.velocity_x

                if abs(distance) < 0.5 and abs(card.velocity_x) < 0.5:
                    x = card.target_x
                    card.velocity_x = 0
                card.loc = (x, y)

        #round overlay logic
        if self.player_knock or self.computer_knock:
            self.context.hand.melds = self.update_melds(self.context.hand)
            self.context.opp_hand.melds = self.update_melds(self.context.opp_hand)
            if self.player_knock:
                player_score, opp_score = self.calculate_round_score(self.context.hand, self.context.opp_hand)
                self.context.hand.score += player_score
                self.context.opp_hand.score += opp_score
                self.player_knock = False
            else:
                opp_score, player_score = self.calculate_round_score(self.context.opp_hand, self.context.hand)
                self.context.hand.score += player_score
                self.context.opp_hand.score += opp_score
                self.computer_knock = False
            self.context.text_renderer.update_score_text(self.context.hand.score, self.context.opp_hand.score)

        #advance the turn
        if (self.player_turn == -1):
            self.computer_play()
            self.sort_cards_rank(self.context.opp_hand)
            self.player_turn *= -1
        if self.manager.restart_from_main_menu:
            self.manager.restart_from_main_menu = False
            self.manager.menu_active = False
            self.context.screen.menu_x = -1.5 * self.context.screen.menu_width
            self.context.screen.hamburger_x = 30
            self.turn = 1
            self.sort_cards_rank(self.context.opp_hand)
            self.manager.set("title")
        if self.manager.restart:
            self.context.reset_round()
            self.manager.restart = False

    def draw(self):
        self.context.drawer.draw_game_background()
        self.context.drawer.draw_menu(self.context.surface_loader.game_surface, self.manager.menu_active, self.context.dt)
        self.context.drawer.draw_buttons()
        self.context.drawer.draw_hand_cards(self.active_card, self.card_hovered)
        self.context.drawer.draw_cards(self.active_card)

        #animations
        if self.context.animator.player_card_flip.active:
            self.context.drawer.draw_player_card_flip(self.drawn_card, self.context.rects.draw_rect.center, (self.context.hand.cards[-1].loc[0] + 73/2, self.context.hand.cards[-1].loc[1] + 98/2))
            self.drawn_card.visible = False
        if self.context.animator.player_card_slide.active:
            self.context.drawer.draw_player_card_slide(self.drawn_card, self.context.rects.discard_rect.center, (self.context.hand.cards[-1].loc[0], self.context.hand.cards[-1].loc[1]))
            self.drawn_card.visible = False
        if self.context.animator.opp_card_flip.active:
            self.context.drawer.draw_opp_card_flip(self.context.rects.discard_rect.center, (self.opp_drawn_card.loc[0] + 73/2, self.opp_drawn_card.loc[1] + 98/2))
        if self.context.animator.opp_card_slide.active:
            self.context.drawer.draw_opp_card_slide(self.context.rects.draw_rect.center, (self.opp_drawn_card.loc[0] + 73/2, self.opp_drawn_card.loc[1] + 98/2))
        if self.context.animator.opp_discard_flip.active:
            self.context.drawer.draw_opp_discard_flip((self.opp_best_discard.loc[0] + 73/2, self.opp_best_discard.loc[1] + 98/2), self.context.rects.discard_rect.center)

        self.context.drawer.draw_round_overlay(self.round_overlay)
        self.context.screen.display_surface.blit(self.context.surface_loader.game_surface, (0,0))

    def exit(self):
        pass

    def enter(self):
        pass

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.manager.running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.manager.running = False
            if event.key == pygame.K_RETURN:
                if self.round_overlay:
                    if self.context.hand.score >= 100 or self.context.opp_hand.score >= 100:
                        print("game over")
                    else:
                        saved_player_score = self.context.hand.score
                        saved_opp_score = self.context.opp_hand.score
                        self.context.reset_round()
                        self.context.hand.score = saved_player_score
                        self.context.opp_hand.score = saved_opp_score
                        self.round_overlay = False
                        self.player_knock = False
                        self.knocking = False
                        self.turn = 1
                        self.player_turn = 1

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.context.rects.menu_rect.collidepoint(event.pos):
                    self.manager.menu_active = True
                if self.context.rects.main_menu_overlay_rect.collidepoint(event.pos):
                    self.manager.menu_active = False
                if self.manager.menu_active:
                    self.context.rects.update_option_rects()
                    if self.context.rects.mm_option_rect.collidepoint(event.pos):
                        self.manager.restart_from_main_menu = True
                    if self.context.rects.qg_option_rect.collidepoint(event.pos):
                        self.manager.running = False
                    if self.context.rects.r_option_rect.collidepoint(event.pos):
                        self.manager.restart = True
                for card in reversed(self.context.hand.cards):
                    if card == self.context.hand.cards[-1]:
                        card_rect = pygame.Rect(card.loc[0], card.loc[1], 73, 98)
                    else:
                        card_rect = pygame.Rect(card.loc[0], card.loc[1], ((self.context.screen.display_surface.get_width() / 3) / (len(self.context.hand.cards) - 1)) * 0.8, 98)
                    if card_rect.collidepoint(event.pos):
                        self.clicked = True
                        self.active_card = card
                        self.active_card.dragging = True
                        self.original_loc = self.active_card.loc
                        self.original_index = self.context.hand.cards.index(self.active_card)
                        self.card_x = event.pos[0] - self.active_card.loc[0]
                        self.card_y = event.pos[1] - self.active_card.loc[1]
                        break
                    elif self.context.rects.draw_rect.collidepoint(event.pos):
                        if self.turn == 1:
                            random.choice(self.context.audio.thwip_sounds).play()
                            self.drawn_card = self.pickup_card(self.context.deck, self.context.hand)
                            self.drawn_card.visible = False
                            self.context.animator.player_card_flip.start()
                            self.context.hand.melds = self.update_melds(self.context.hand)
                            if self.can_knock(self.context.hand.melds, self.context.hand.cards):
                                self.context.hand.can_knock = True
                            self.turn *= -1
                            break
                    elif self.context.rects.discard_rect.collidepoint(event.pos):
                        if self.turn == 1:
                            self.context.audio.slide_sound.play()
                            self.drawn_card = self.pickup_discard(self.context.hand)
                            self.context.animator.player_card_slide.start()
                            #self.drawn_card = None
                            #self.horizontal_shift = (((self.context.screen.display_surface.get_width() / 3) / len(self.context.hand.cards)) * 0.8)
                            self.context.hand.melds = self.update_melds(self.context.hand)
                            if self.can_knock(self.context.hand.melds, self.context.hand.cards):
                                self.context.hand.can_knock = True
                            if self.context.discard_pile.cards:
                            #    discard_top = pygame.image.load(f'./assets/cards/{discard_pile.cards[-1].name}')
                                self.discard_top = self.context.image_loader.card_images[self.context.discard_pile.cards[-1].name]
                                pass
                            self.turn *= -1
                            break
                    elif self.context.rects.sort_rect_rank.collidepoint(event.pos):
                        self.sort_cards_rank(self.context.hand)
                    elif self.context.rects.sort_rect_suit.collidepoint(event.pos):
                        self.sort_cards_suit(self.context.hand)
                    elif self.context.rects.player_knock_rect.collidepoint(event.pos):
                        self.knocking = True
        elif event.type == pygame.MOUSEMOTION and self.clicked == True:
            if self.active_card:
                self.active_card.loc = (event.pos[0] - self.card_x, event.pos[1] - self.card_y)
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.active_card:
                self.active_card.dragging = False
                starting_hover_index = None

                if self.original_loc[0] > self.active_card.loc[0]:
                    for i, card in enumerate(self.context.hand.cards):
                        starting_hover_index = i
                        break
                    if starting_hover_index is None:
                        starting_hover_index = self.original_index
                    placeholder = self.active_card
                    for i in range(self.original_index, starting_hover_index, -1):
                        self.context.hand.cards[i] = self.context.hand.cards[i-1]
                    self.context.hand.cards[starting_hover_index] = placeholder
                elif self.original_loc[0] < self.active_card.loc[0]:
                    for i in range(len(self.context.hand.cards)-1, -1, -1):
                        if self.context.hand.cards[i].hovered_x and self.context.hand.cards[i] != self.active_card:
                            starting_hover_index = i
                            break
                    if starting_hover_index is None:
                        starting_hover_index = self.original_index
                    placeholder = self.active_card
                    for i in range(self.original_index, starting_hover_index, 1):
                        self.context.hand.cards[i] = self.context.hand.cards[i+1]
                    self.context.hand.cards[starting_hover_index] = placeholder

                if self.context.rects.discard_rect.collidepoint(event.pos) and self.turn == -1:
                    self.discard(self.context.hand, self.active_card)
                    if self.knocking:
                        self.round_overlay = True
                        self.player_knock = True
                        self.knocking = False
                    else:
                        self.turn *= -1
                        self.player_turn *= -1
                for card in self.context.hand.cards:
                    card.hovered_x = False
                self.active_card = None
                self.clicked = False
        
    def pickup_card(self, deck, hand): #replaced drawCard()
        choice = random.choice(deck.cards)
        hand.cards.append(choice)
        deck.cards.remove(choice)
        return choice
    
    def sort_cards_rank(self, hand):
        sorted_hand = []
        greatest_card = None
        while hand.cards:
            greatest_num = 0
            for card in hand.cards:
                if self.context.card_data[card.name]["rank"] >= greatest_num:
                    greatest_num = self.context.card_data[card.name]["rank"]
                    greatest_card = card
            hand.cards.remove(greatest_card)
            sorted_hand.append(greatest_card)
        hand.cards = sorted_hand

    def sort_cards_suit(self, hand):
        self.sort_cards_rank(hand)
        suitgroups = defaultdict(list)
        sorted_hand = []
        for card in hand.cards:
            suitgroups[self.context.card_data[card.name]["suit"]].append(card)
        
        for cards in suitgroups.values():
            for card in cards:
                sorted_hand.append(card)
        hand.cards = sorted_hand
    
    def discard(self, hand, active_card):
        hand.cards.remove(active_card)
        self.context.discard_pile.cards.append(active_card)

    def pickup_discard(self, hand):
        choice = self.context.discard_pile.cards[-1]
        hand.cards.append(choice)
        self.context.discard_pile.cards.remove(choice)
        return choice

    def can_knock(self, melds, cards):
        meld_cards = []
        for meld in melds:
            for card in meld:
                meld_cards.append(card)

        greatest_deadwood = 0
        total_deadwood = 0
        for card in cards:
            if card not in meld_cards:

                if self.context.card_data[card.name]["rank"] > 10:
                    total_deadwood += 10
                else:
                    total_deadwood += self.context.card_data[card.name]["rank"]
                
                if self.context.card_data[card.name]["rank"] > greatest_deadwood:
                    greatest_deadwood = self.context.card_data[card.name]["rank"]
        
        if total_deadwood - greatest_deadwood <= 10:
            return True
        else:
            return False
    
    def update_melds(self, this_hand):
        rank_groups = defaultdict(list)
        suit_groups = defaultdict(list)
        for card in this_hand.cards:
            rank = self.context.card_data[card.name]["rank"]
            suit = self.context.card_data[card.name]["suit"]
            rank_groups[rank].append(card)
            suit_groups[suit].append((rank, card))
        all_melds = []
        for cards in rank_groups.values():
            if len(cards) >= 3:
                all_melds.append(cards[:])
                if len(cards) == 4:
                    for i in range(4):
                        all_melds.append([c for j, c in enumerate(cards) if j != i])
        for suit, cards in suit_groups.items():
            cards.sort()
            run = [cards[0][1]]
            for i in range(1, len(cards)):
                if cards[i][0] == cards[i - 1][0] + 1:
                    run.append(cards[i][1])
                else:
                    if len(run) >= 3:
                        for start in range(len(run)):
                            for end in range(start + 3, len(run) + 1):
                                all_melds.append(run[start:end])
                    run = [cards[i][1]]
            if len(run) >= 3:
                for start in range(len(run)):
                    for end in range(start + 3, len(run) + 1):
                        all_melds.append(run[start:end])
        if not all_melds:
            return []
        best_melds = []
        best_deadwood = 100
        for r in range(1, len(all_melds) + 1):
            for combo in combinations(all_melds, r):
                used = set()
                valid = True
                for meld in combo:
                    for card in meld:
                        if card in used:
                            valid = False
                            break
                    if not valid:
                        break
                    used.update(meld)
                if valid:
                    deadwood = 0
                    for card in this_hand.cards:
                        if card not in used:
                            deadwood += min(self.context.card_data[card.name]["rank"], 10)
                    if deadwood < best_deadwood:
                        best_deadwood = deadwood
                        best_melds = list(combo)
        return best_melds

    def calculate_round_score(self, knocker_hand, defender_hand):
        #knocker_melds = update_melds(knocker_hand)
        #defender_melds = update_melds(defender_hand)
        
        #knocker_deadwood = calculate_deadwood(knocker_melds, knocker_hand.cards)
        knocker_deadwood = self.calculate_deadwood(knocker_hand.melds, knocker_hand.cards)
        
        # only consider cards that are actually deadwood for the defender
        defender_meld_cards = [card for meld in defender_hand.melds for card in meld]
        defender_deadwood_cards = [card for card in defender_hand.cards if card not in defender_meld_cards]
        
        # lay off defender's deadwood onto knocker's melds
        # skip layoff entirely if knocker has gin
        laid_off = []
        if knocker_deadwood > 0:
            for meld in knocker_hand.melds:
                for card in defender_deadwood_cards:
                    if self.can_contribute(card, meld) and card not in laid_off:
                        laid_off.append(card)

        # calculate defender's remaining deadwood after layoffs
        defender_deadwood_score = sum(
            min(self.contextcard_data[card.name]["rank"], 10)
            for card in defender_deadwood_cards
            if card not in laid_off
        )
        
        if defender_deadwood_score <= knocker_deadwood:  # undercut
            return 0, (knocker_deadwood - defender_deadwood_score) + 25
        else:
            return defender_deadwood_score - knocker_deadwood, 0

    def calculate_deadwood(self, melds, cards):
        deadwood = 0
        meld_cards = []
        for meld in melds:
            for card in meld:
                meld_cards.append(card)
        for card in cards:
            if card not in meld_cards:
                deadwood += min(self.context.card_data[card.name]["rank"], 10)
        return deadwood
    
    def can_contribute(self, card, meld):
        type = self.get_meld_type(meld)
        if type == "run":
            if self.context.card_data[card.name]["suit"] == self.context.card_data[meld[0].name]["suit"]:
                if self.context.card_data[card.name]["rank"] == self.context.card_data[meld[0].name]["rank"] - 1:
                    return True
                elif self.context.card_data[card.name]["rank"] == self.context.card_data[meld[-1].name]["rank"] + 1:
                    return True
        elif type == "set":
            if self.context.card_data[card.name]["rank"] == self.context.card_data[meld[0].name]["rank"]:
                return True
        return False

    def get_meld_type(self, meld):
        if self.context.card_data[meld[0].name]["rank"] == self.context.card_data[meld[1].name]["rank"]:
            return "set"
        elif (abs(self.context.card_data[meld[0].name]["rank"] - self.context.card_data[meld[1].name]["rank"]) == 1 and self.context.card_data[meld[0].name]["suit"] == self.context.card_data[meld[1].name]["suit"]):
            return "run"
        else:
            return "none"

    def computer_play(self):
        self.context.opp_hand.melds = self.update_melds(self.context.opp_hand)
        current_deadwood = self.calculate_deadwood(self.context.opp_hand.melds, self.context.opp_hand.cards)

        discard_card = self.context.discard_pile.cards[-1]
        self.context.opp_hand.cards.append(discard_card)
        simulated_melds = self.update_melds(self.context.opp_hand)
        simulated_deadwood = self.calculate_deadwood(simulated_melds, self.context.opp_hand.cards)
        self.context.opp_hand.cards.remove(discard_card)

        pickup_dis = False
        if simulated_deadwood < current_deadwood:
            self.opp_drawn_card = self.pickup_discard(self.context.opp_hand)
            pickup_dis = True
        else:
            self.opp_drawn_card = self.pickup_card(self.context.deck, self.context.opp_hand)
        
        #animate card movement
        if pickup_dis:
            self.context.animator.opp_card_flip.start()
        else:
            self.context.animator.opp_card_slide.start()
        #update melds after pickup
        self.context.opp_hand.melds = self.update_melds(self.context.opp_hand)
        
        self.opp_best_discard = None
        best_deadwood = float('inf')

        for card in self.context.opp_hand.cards:
            in_meld = any(card in meld for meld in self.context.opp_hand.melds)
            if in_meld:
                continue
            
            self.context.opp_hand.cards.remove(card)
            simulated_melds = self.update_melds(self.context.opp_hand)
            simulated_deadwood = self.calculate_deadwood(simulated_melds, self.context.opp_hand.cards)
            self.context.opp_hand.cards.append(card)

            if simulated_deadwood < best_deadwood:
                best_deadwood = simulated_deadwood
                self.opp_best_discard = card

        if self.opp_best_discard is None:
            self.opp_best_discard = self.context.opp_hand.cards[-1]
        self.context.animator.opp_discard_flip.start()
        self.discard(self.context.opp_hand, self.opp_best_discard)

        self.context.opp_hand.melds = self.update_melds(self.context.opp_hand)
        deadwood = self.calculate_deadwood(self.context.opp_hand.melds, self.context.opp_hand.cards)

        if deadwood == 0:
            self.context.opp_hand.can_knock = True
            self.context.opp_hand.can_gin = True
        elif deadwood <= 10:
            self.context.opp_hand.can_knock = True
            self.context.opp_hand.can_gin = False
        
        if self.context.opp_hand.can_gin or self.context.opp_hand.can_knock:
            global round_overlay, computer_knock
            round_overlay = True
            computer_knock = True
            self.context.opp_hand.can_knock = False
            self.context.opp_hand.can_gin = False

    def update_card_hover(self):
        mouse_pos = pygame.mouse.get_pos()
        
        newly_hovered = None
        for card in reversed(self.context.hand.cards):
            width = 73 if card == self.context.hand.cards[-1] else (self.context.screen.display_surface.get_width() / 3) / max(len(self.context.hand.cards) - 1, 1) * 0.8
            rect = pygame.Rect(int(card.loc[0]), int(card.base_y), int(width), 98)
            if rect.collidepoint(mouse_pos):
                newly_hovered = card
                break

        if newly_hovered != self.card_hovered:
            self.card_hovered = newly_hovered

        for card in self.context.hand.cards:
            card.target_y = card.base_y - 50 if card == self.card_hovered else card.base_y

        for card in self.context.hand.cards:
            if card.dragging:
                continue
            x, y = card.loc
            distance = card.target_y - y
            card.velocity_y += distance * 0.15
            card.velocity_y *= 0.6
            y += card.velocity_y
            if abs(distance) < 0.1 and abs(card.velocity_y) < 0.1:
                y = card.target_y
                card.velocity_y = 0
            card.loc = (x, y)