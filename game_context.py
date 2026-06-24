from context.game_components.deck import Deck
from context.game_components.hand import Hand
from context.game_components.discard_pile import DiscardPile
from context.engine.managers.drawer import Drawer
from context.engine.managers.animator import Animator
from context.engine.monitor_setup import Monitor
from context.engine.audio import Audio
from context.engine.screen import Screen
import pygame

class GameContext:
    def __init__(self):
        #game components
        deck = Deck()
        self.hand = Hand(deck)
        self.opp_hand = Hand(deck)
        self.discard_pile = DiscardPile(deck)

        #engine components
        self.clock = pygame.time.Clock()
        self.audio = Audio()
        self.monitor = Monitor()
        self.screen = Screen()
        self.drawer = Drawer(self.screen)
        self.animator = Animator(self.drawer)



