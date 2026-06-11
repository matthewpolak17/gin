import pygame
import csv
import os
from screeninfo import get_monitors
from deck import Deck
from hand import Hand
from discard_pile import DiscardPile

class Game:
    def __init__(self):
        self._setup_monitor()
        self._setup_screen()
        self._setup_game_variables()
        self._setup_constants()
        self._setup_fonts()
        self._setup_sfx()
        self._setup_assets()
        self._setup_ui()

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
        self.deck = Deck()
        self.hand = Hand(self.deck)
        self.opp_hand = Hand(self.deck)
        self.discard_pile = DiscardPile(self.deck)

    def _setup_constants(self):
        self.card_images = {}
        self.card_data = {}
        self.wipe_speed = 70
        self.card_movement_speed = 600
        self.WHITE = (255,255,255)
        self.BLACK = (0,0,0)

    def _setup_fonts(self):
        self.large_font = pygame.font.Font(None, 50)
        self.medium_font = pygame.font.Font(None, 35)
        self.small_font = pygame.font.Font(None, 30)

    def _setup_sfx(self):
        pygame.mixer.init()
        self.thwip_sounds = [
            pygame.mixer.Sound("./assets/sfx/thwip3.wav"),
            pygame.mixer.Sound("./assets/sfx/thwip4.wav"),
            pygame.mixer.Sound("./assets/sfx/thwip5.wav"),
            ]
        self.shuffle_sound = pygame.mixer.Sound("./assets/sfx/shuffle.wav")
        self.slide_sound = pygame.mixer.Sound("./assets/sfx/slide1.wav")
    
    def _setup_assets(self):
        #images loaded here
        self.discard_top = pygame.image.load(f'./assets/cards/{self.discard_pile.cards[-1].name}')
        self.icon = pygame.image.load(f'./assets/icon.png').convert_alpha()
        self.background = pygame.image.load(r'./assets/background.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (self.native_width, self.native_height))
        self.blue_back = pygame.transform.scale(pygame.image.load(r'./assets/blueback.png'), (73, 98))
        self.title_background = pygame.image.load(f'./assets/title_background.png').convert_alpha()
        self.tb_width = self.title_background.get_width()
        pygame.display.set_icon(self.icon)

        #card_data is filled here
        with open('./assets/card_values.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.card_data[row['name']] = {'suit': row['suit'], 'rank': int(row['rank'])}

        images = {}
        for name in self.card_data:
            img = pygame.image.load(f'./assets/cards/{name}').convert_alpha()
            images[name] = pygame.transform.smoothscale(img, (73, 98))
        self.card_images = images

        print("assets loaded")

    def _setup_menu(self):
        self.hamburger_x = 30
        self.hamburger_width = 50
        self.hamburger_tx = -1.5 * self.hamburger_width

        self.menu_rect = pygame.Rect(20,20,70,58)
        self.menu_width = self.display_surface.get_width() / 8
        self.menu_x = -1.5 * self.menu_width
        self.menu_tx = 0
        self.menu_speed = 2600
        self.menu_overlay = False
        self.main_menu_overlay_rect = pygame.Rect(self.menu_width, 0, self.display_surface.get_width() - self.menu_width, self.displayHeight)

        self.side_overlay = pygame.Surface((self.menu_width, self.displayHeight), pygame.SRCALPHA)
        self.side_overlay.fill((0, 0, 0,  80))

        self.start_text = self.small_font.render("Press ENTER to Start", True, (255,222,133))
        self.start_rect = self.start_text.get_rect(center=(self.displayWidth // 2, self.displayHeight // 2))

    def _setup_ui(self):
        #sorting buttons
        self.sort_rect_rank = pygame.Rect(self.displayWidth * 2/3, self.displayHeight * 0.75, 80, 40)
        self.sort_rect_suit = pygame.Rect(self.displayWidth * 2/3, self.displayHeight * 0.8, 80, 40)
        self.sort_rank_text = self.small_font.render("Rank", True, self.BLACK)
        self.sort_suit_text = self.small_font.render("Suit", True, self.BLACK)
        self.sort_rank_rect = self.ort_rank_text.get_rect(center=self.sort_rect_rank.center)
        self.sort_suit_rect = self.sort_suit_text.get_rect(center=self.sort_rect_suit.center)

        #knocking buttons
        self.player_knock_rect = pygame.Rect(self.displayWidth * 2/3, self.displayHeight * 0.70, 80, 40)
        self.opp_knock_rect = pygame.Rect(self.displayWidth * 2/3, self.displayHeight * 0.2, 80, 40)
        self.player_knock_text = self.small_font.render("Knock", True, self.BLACK)
        self.opp_knock_text = self.small_font.render("Knock", True, self.BLACK)
        self.knock_player_rect = self.player_knock_text.get_rect(center=self.player_knock_rect.center)
        self.knock_opp_rect = self.opp_knock_text.get_rect(center=self.opp_knock_rect.center)

        self.draw_rect = pygame.Rect(self.display_surface.get_width() * 4/9 - self.blue_back.get_width() / 2, self.display_surface.get_height() / 2 - self.blue_back.get_height() / 2, 73, 98)
        self.knock_rect = pygame.Rect(self.display_surface.get_width() - 60, self.display_surface.get_height() - 30, 30, 10)
        self.opp_knock_rect = pygame.Rect(self.display_surface.get_width() - 60, self.isplay_surface.get_height() - 90, 30, 10)
        self.discard_rect = pygame.Rect(self.display_surface.get_width() * 5/9 - self.blue_back.get_width() / 2, self.display_surface.get_height() / 2 - self.blue_back.get_height() / 2, 73, 98)

        #text
        self.player_score_text = None
        self.opp_score_text = None
        print("ui setup")



