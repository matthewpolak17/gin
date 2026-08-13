from context.game_components.deck import Deck
from context.game_components.hand import Hand
from context.game_components.discard_pile import DiscardPile
from context.engine.managers.drawer import Drawer
from context.engine.managers.title_drawer import TitleDrawer
from context.engine.managers.animator import Animator
from context.engine.managers.title_animator import TitleAnimator
from context.engine.managers.text_renderer import TextRenderer
from context.engine.managers.image_loader import ImageLoader
from context.engine.managers.surface_loader import SurfaceLoader
from context.engine.ui_text import UI_Text
from context.engine.rects import Rects
from context.engine.monitor_setup import Monitor
from context.engine.audio import Audio
from context.engine.screen import Screen
from context.engine import constants
import pygame
import csv

class GameContext:
    def __init__(self):
        #game components
        self.deck = Deck()
        self.hand = Hand(self.deck)
        self.opp_hand = Hand(self.deck)
        self.discard_pile = DiscardPile(self.deck)

        #engine components
        self.card_data = {}
        with open('./assets/card_values.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.card_data[row['name']] = {'suit': row['suit'], 'rank': int(row['rank'])}

        self.constants = constants
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.audio = Audio(self)
        self.monitor = Monitor(self)
        self.screen = Screen(self)
        self.ui_text = UI_Text(self)
        self.drawer = Drawer(self)
        self.title_drawer = TitleDrawer(self)
        self.animator = Animator(self)
        self.title_animator = TitleAnimator(self)
        self.text_renderer = TextRenderer(self)
        self.image_loader = ImageLoader(self)
        self.rects = Rects(self)
        self.surface_loader = SurfaceLoader(self)


    def reset_round(self):
        self.deck = Deck()
        self.hand = Hand(self.deck)
        self.opp_hand = Hand(self.deck)
        self.discard_pile = DiscardPile(self.deck)
        self.text_renderer.player_score_text = None
        self.text_renderer.opp_score_text = None
        self.updateLocations()

    def updateLocations(self):
        def set_card_positions(cards, y_offset, spacing_scale=self.constants.CARD_SPACING):
            win_width = self.screen.display_surface.get_width()
            max_spacing = (win_width / 3) / len(cards)
            if len(cards) == 11:
                spacing_scale *= 0.99
            spacing = max_spacing * spacing_scale
            total_width = spacing * (len(cards) - 1)
            start_x = (win_width - total_width) / 2 - 36

            for x, card in enumerate(cards):
                if card.dragging:
                    continue
                x_pos = start_x + x * spacing
                y_pos = y_offset
                card.base_x = x_pos
                card.target_x = x_pos
                #print(x_pos)
                card.loc = (x_pos, y_pos)
                card.base_y = y_pos
                card.target_y = y_pos

        mid_y = self.screen.display_surface.get_height() / 2
        set_card_positions(self.hand.cards, 1.5 * mid_y)
        set_card_positions(self.opp_hand.cards, 0.5 * mid_y - 98)


        #win_width = 1920
        # max_spacing = (win_width / 3) / 10
        # spacing = max_spacing * 0.8
        # total_width = spacing * (10 - 1)
        # start_x = (win_width - total_width) / 2 - 36

        # for i in range(10):
        #     print("10 card spacing: " + str(start_x + i * spacing))

        # max_spacing = (win_width / 3) / 11
        # spacing = max_spacing * 0.792
        # total_width = spacing * (11 - 1)
        # start_x = (win_width - total_width) / 2 - 36

        # for i in range(11):
        #     print("11 card spacing: " + str(start_x + i * spacing))






