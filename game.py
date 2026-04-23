import pygame
import random
import csv
import os
from itertools import combinations
from screeninfo import get_monitors
from collections import defaultdict
from deck import Deck
from hand import Hand
from discard_pile import DiscardPile

class Game:
    def __init__(self):
        self.setup_monitor()
        self._setup_screen()
        self._setup_game_variables()
        self._setup_fonts()
        self.sfx_setup()
        self._setup_constants()
        self._setup_assets()
        self.setup_ui()
        self.reset_round()

    def _setup_monitor(self):
        monitors = get_monitors()
        second_monitor = monitors[0]
        os.environ['SDL_VIDEO_WINDOW_POS'] = f"{second_monitor.x},{second_monitor.y}"
    def _setup_screen(self):
            pygame.init()
            pygame.display.set_caption("Gin Rummy")
            info = pygame.display.Info()
            flags = pygame.NOFRAME | pygame.HWSURFACE | pygame.DOUBLEBUF
            self.displayWidth, self.displayHeight = info.current_w, info.current_h
            self.display_surface = pygame.display.set_mode((self.displayWidth, self.displayHeight), flags)
            self.title_surface = pygame.Surface((self.displayWidth, self.displayHeight))
            self.game_surface = pygame.Surface((self.displayWidth, self.displayHeight))
            print("screen setup")
    def _setup_game_variables(self):
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.running = True
        self.dropped = False
        self.clicked = False
        self.round_overlay = False
        self.player_knock = False
        self.computer_knock = False
        self.card_flip = False
        self.drawn_card = None
        self.opp_drawn_card = None
        self.original_index = None
        self.turn = 1
        self.player_turn = 1
        self.knocking = False
        self.restart_from_main_menu = False
        self.restart = False
    def _setup_fonts(self):
        self.large_font = pygame.font.Font(None, 50)
        self.medium_font = pygame.font.Font(None, 35)
        self.small_font = pygame.font.Font(None, 30)
    def _setup_constants(self):
        self.card_images = {}
        self.card_data = {}
        self.wipe_speed = 70
        self.card_movement_speed = 600
        self.WHITE = (255,255,255)
        self.BLACK = (0,0,0)
    def _setup_assets(self):

    def sfx_setup(self):
        pygame.mixer.init()
        self.thwip_sounds = [
            pygame.mixer.Sound("./assets/sfx/thwip3.wav"),
            pygame.mixer.Sound("./assets/sfx/thwip4.wav"),
            pygame.mixer.Sound("./assets/sfx/thwip5.wav"),
            ]
        self.shuffle_sound = pygame.mixer.Sound("./assets/sfx/shuffle.wav")
        self.slide_sound = pygame.mixer.Sound("./assets/sfx/slide1.wav")

    def reset_round(self):
        self.deck = Deck()
        self.hand = Hand(self.deck)
        self.opp_hand = Hand(self.deck)
        self.discard_pile = DiscardPile(self.deck)
        self.turn = 1
        self.player_turn = 1
        self.round_overlay = False
        self.player_knock = False
        self.computer_knock = False
        self.knocking = False
        print("new round started")
    

    def setup_assets(self):
        print("assets setup")

    def setup_ui(self):
        print("ui setup")

    def run(self):
        print("game started")



