from context.game_components.deck import Deck
from context.game_components.hand import Hand
from context.game_components.discard_pile import DiscardPile
from context.engine.managers.drawer import Drawer
from context.engine.managers.animator import Animator
from context.engine.managers.text_renderer import TextRenderer
from context.engine.managers.image_loader import ImageLoader
from context.engine.managers.surface_loader import SurfaceLoader
from context.engine.monitor_setup import Monitor
from context.engine.audio import Audio
from context.engine.screen import Screen
from context.engine import constants
import pygame
import csv

class GameContext:
    def __init__(self):
        #game components
        deck = Deck()
        self.hand = Hand(deck)
        self.opp_hand = Hand(deck)
        self.discard_pile = DiscardPile(deck)

        #engine components
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.audio = Audio(self)
        self.monitor = Monitor(self)
        self.screen = Screen(self)
        self.drawer = Drawer(self)
        self.animator = Animator(self)
        self.text_renderer = TextRenderer(self)
        self.image_loader = ImageLoader(self)
        self.surface_loader = SurfaceLoader(self)
        self.constants = constants
        self.card_data = {}
        with open('./assets/card_values.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.card_data[row['name']] = {'suit': row['suit'], 'rank': int(row['rank'])}

    def reset_round(self):
        self.deck = Deck()
        self.hand = Hand(self.deck)
        self.opp_hand = Hand(self.deck)
        self.discard_pile = DiscardPile(self.deck)
        self.text_renderer.player_score_text = None
        self.text_renderer.opp_score_text = None




