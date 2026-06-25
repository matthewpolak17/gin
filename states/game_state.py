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
        self.original_loc = (0,0)
        self.original_index = None
        self.turn = 1
        self.drawn_card = None
        self.knocking = False
        self.horizontal_shift = (((self.context.screen.display_surface.get_width() / 3) / len(self.context.hand.cards)) * 0.8)
        self.player_knock = False
        self.round_overlay = False

    def update(self):
        pass

    def draw(self):
        pass

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
                if self.manager.engine.drawer.menu_rect.collidepoint(event.pos):
                    self.manager.menu_active = True
                if self.manager.engine.drawer.main_menu_overlay_rect.collidepoint(event.pos):
                    self.manager.menu_active = False
                if self.manager.menu_active:
                    self.context.drawer.rects.update_option_rects()
                    if self.context.drawer.rects.mm_option_rect.collidepoint(event.pos):
                        self.manager.restart_from_main_menu = True
                    if self.context.drawer.rects.qg_option_rect.collidepoint(event.pos):
                        self.manager.running = False
                    if self.context.drawer.rects.r_option_rect.collidepoint(event.pos):
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
                        card_x = event.pos[0] - self.active_card.loc[0]
                        card_y = event.pos[1] - self.active_card.loc[1]
                        break
                    elif self.context.drawer.draw_rect.collidepoint(event.pos):
                        if self.turn == 1:
                            random.choice(self.context.audio.thwip_sounds).play()
                            self.drawn_card = self.pickup_card(self.context.deck, self.context.hand)
                            self.drawn_card.visible = False
                            self.context.animator.animate_player_card_flip(self.drawn_card, self.context.drawer.draw_rect.center, (self.context.hand.cards[-1].loc[0] + 73/2, self.context.hand.cards[-1].loc[1] + 98/2))
                            self.drawn_card = None
                            self.context.hand.melds = self.update_melds(self.context.hand)
                            if self.can_knock(self.context.hand.melds, self.context.hand.cards):
                                self.context.hand.can_knock = True
                            self.turn *= -1
                            break
                    elif self.context.drawer.rects.sort_rect_rank.collidepoint(event.pos):
                        self.sort_cards_rank(self.context.hand)
                    elif self.context.drawer.rects.sort_rect_suit.collidepoint(event.pos):
                        self.sort_cards_suit(self.context.hand)
                    elif self.context.drawer.rects.player_knock_rect.collidepoint(event.pos):
                        self.knocking = True
        elif event.type == pygame.MOUSEMOTION and self.clicked == True:
            if self.active_card:
                self.active_card.loc = (event.pos[0] - card_x, event.pos[1] - card_y)
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

                if self.context.drawer.rects.discard_rect.collidepoint(event.pos) and self.turn == -1:
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
        self.updateLocations()         

    def pickup_card(self, deck, hand): #replaced drawCard()
        choice = random.choice(deck.cards)
        hand.cards.append(choice)
        deck.cards.remove(choice)
        #load_hand()
        #self.updateLocations()
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

    def updateLocations(self):
        def set_card_positions(cards, y_offset, spacing_scale = self.context.constants.CARD_SPACING):
            win_width = self.context.screen.display_surface.get_width()
            max_spacing = (win_width / 3) / len(cards)
            spacing = max_spacing * spacing_scale
            total_width = spacing * (len(cards) - 1)
            start_x = (win_width - total_width) / 2 - 36

            for x, card in enumerate(cards):
                x_pos = start_x + x * spacing
                y_pos = y_offset
                card.loc = (x_pos, y_pos)
                card.base_y = y_pos
                card.target_y = y_pos
                card.base_x = x_pos
                card.target_x = x_pos

        mid_y = self.context.screen.display_surface.get_height() / 2
        set_card_positions(self.context.hand.cards, 1.5 * mid_y)
        set_card_positions(self.context.opp_hand.cards, 0.5 * mid_y - 98)


