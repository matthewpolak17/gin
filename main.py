#--------- Glossary ---------
# [WIP] -> Work in Progress
# [RL]  -> Remove Later
# [DB]  -> Debugging

import pygame
import random
import csv
import constants
from itertools import combinations
from collections import defaultdict
from deck import Deck
from hand import Hand
from discard_pile import DiscardPile
from monitor_setup import Monitor
from mixer import Mixer
from ui_elements.text_renderer import TextRenderer
from screen import Screen
from ui_elements.rects import Rects
#from assets.loaders.image_loader import ImageLoader
#from assets.loaders.surface_loader import SurfaceLoader
from drawer import Drawer
from animator import Animator


pygame.init()

monitor = Monitor()
screen = Screen()
mixer = Mixer()
#text_renderer = TextRenderer()
#rects = Rects(screen, text_renderer)
#image_loader = ImageLoader(screen)
#surface_loader = SurfaceLoader(screen)
drawer = Drawer(screen)
animator = Animator(drawer)
clock = pygame.time.Clock()

deck = Deck()
hand = Hand(deck)
discard_pile = DiscardPile(deck)
opp_hand = Hand(deck)

#screen setup
#pygame.init()
#screen.display_height = monitor.screen.display_height
#screen.display_width = monitor.screen.display_width
#flags = pygame.NOFRAME | pygame.HWSURFACE | pygame.DOUBLEBUF
#screen.display_surface = pygame.display.set_mode((screen.display_width, screen.display_height), flags)
#pygame.display.set_caption("Gin Rummy")
#clock = pygame.time.Clock()
#screen.display_height = screen.display_height
#screen.display_width = screen.display_width
#title_surface = pygame.Surface((screen.display_width, screen.display_height))
#game_surface = pygame.Surface((screen.display_width, screen.display_height))
#networking_surface = pygame.Surface((screen.display_width, screen.display_height))


#game variables
running = True
dropped = False
clicked = False
round_overlay = False
player_knock = False
computer_knock = False
card_flip = False
original_loc = (0, 0)
horizontal_shift = (((screen.display_surface.get_width() / 3) / len(hand.cards)) * 0.8) #determines how far to hover cards horizontally
#discard_top = None
active_card = None
#card_images = {}
card_data = {}
dt = 0
drawn_card = None
opp_drawn_card = None
original_index = None
turn = 1
player_turn = 1
knocking = False
restart_from_main_menu = False
restart = False
# large_font = pygame.font.Font(None, 50)
# medium_font = pygame.font.Font(None, 35)
# small_font = pygame.font.Font(None, 30)
constants.TITLE_WIPE_SPEED = 40
#card_movement_speed = 600
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)

#menu variables
#hamburger_x = 30
#hamburger_width = 50
#hamburger_tx = -1.5 * hamburger_width

#menu_rect = pygame.Rect(20,20,70,58)
#menu_width = screen.display_surface.get_width() / 8
#menu_x = -1.5 * screen.menu_width
#menu_speed = 2600
menu_active = False
#main_menu_overlay_rect = pygame.Rect(screen.menu_width, 0, screen.display_surface.get_width() - screen.menu_width, screen.display_height)

#side_overlay = pygame.Surface((screen.menu_width, screen.display_height), pygame.SRCALPHA)
#side_overlay.fill((0, 0, 0,  80))

#start_text = small_font.render("Press ENTER to Start", True, (255,222,133))
#start_rect = text_renderer.start_text.get_rect(center=(screen.display_width // 2, screen.display_height // 2))

#multiplayer_text = small_font.render("Press SHIFT for Multiplayer", True, (255,222,133))
#multiplayer_rect = text_renderer.multiplayer_text.get_rect(center=(screen.display_width // 2, screen.display_height // 1.85))

#multiplayer_menu_text = small_font.render("Start a room here", True, WHITE)
#multiplayer_menu_rect = text_renderer.multiplayer_menu_text.get_rect(center=(screen.display_width // 2, screen.display_height // 2))

#sorting buttons
# sort_rect_rank = pygame.Rect(screen.display_width * 2/3, screen.display_height * 0.75, 80, 40)
# sort_rect_suit = pygame.Rect(screen.display_width * 2/3, screen.display_height * 0.8, 80, 40)
#sort_rank_text = small_font.render("Rank", True, BLACK)
#sort_suit_text = small_font.render("Suit", True, BLACK)
#get rid of these two below
# sort_rank_rect = text_renderer.sort_rank_text.get_rect(center=sort_rect_rank.center)
# sort_suit_rect = text_renderer.sort_suit_text.get_rect(center=sort_rect_suit.center)

#knocking buttons
#player_knock_rect = pygame.Rect(screen.display_width * 2/3, screen.display_height * 0.70, 80, 40)
#opp_knock_rect = pygame.Rect(screen.display_width * 2/3, screen.display_height * 0.2, 80, 40)
#player_knock_text = small_font.render("Knock", True, BLACK)
#opp_knock_text = small_font.render("Knock", True, BLACK)


#images loaded here
#discard_top = pygame.image.load(f'./assets/cards/{discard_pile.cards[-1].name}')
#icon = pygame.image.load(f'./assets/icon.png').convert_alpha()
#background = pygame.image.load(r'./assets/background.png').convert_alpha()
#background = pygame.transform.scale(background, (screen.display_width, screen.display_height))
# networking_background = pygame.image.load(r'./assets/networking_background.jpg').convert_alpha()
# networking_background = pygame.transform.scale(networking_background, (screen.display_width, screen.display_height))
#blue_back = pygame.transform.scale(pygame.image.load(r'./assets/blueback.png'), (73, 98))
#title_background = pygame.image.load(f'./assets/title_background.png').convert_alpha()
#title_background = pygame.transform.scale(title_background, (screen.display_width, screen.display_height))
#tb_width = image_loader.title_background.get_width()
#pygame.display.set_icon(icon)

#card_data is filled here
with open('./assets/card_values.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        card_data[row['name']] = {'suit': row['suit'], 'rank': int(row['rank'])}

drawer.image_loader.create_card_images(card_data)

#all card images loaded here
# card_images = {}
# for name in card_data:
#     img = pygame.image.load(f'./assets/cards/{name}').convert_alpha()
#     card_images[name] = pygame.transform.smoothscale(img, (constants.CARD_WIDTH, constants.CARD_HEIGHT))

#rects
#draw_rect = pygame.Rect(screen.display_surface.get_width() * 4/9 - blue_back.get_width() / 2, screen.display_surface.get_height() / 2 - blue_back.get_height() / 2, 73, 98)
#knock_rect = pygame.Rect(screen.display_surface.get_width() - 60, screen.display_surface.get_height() - 30, 30, 10)
#opp_knock_rect = pygame.Rect(screen.display_surface.get_width() - 60, screen.display_surface.get_height() - 90, 30, 10)
#discard_rect = pygame.Rect(screen.display_surface.get_width() * 5/9 - blue_back.get_width() / 2, screen.display_surface.get_height() / 2 - blue_back.get_height() / 2, 73, 98)

#knock_player_rect = text_renderer.player_knock_text.get_rect(center=rects.player_knock_rect.center)
#knock_opp_rect = text_renderer.opp_knock_text.get_rect(center=rects.opp_knock_rect.center)

#text
#player_score_text = None
#opp_score_text = None



#comment out here up for tempmain.py

#functions
def updateLocations():
    def set_card_positions(cards, y_offset, spacing_scale=0.8):
        win_width = screen.display_surface.get_width()
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

    mid_y = screen.display_surface.get_height() / 2
    set_card_positions(hand.cards, 1.5 * mid_y)
    set_card_positions(opp_hand.cards, 0.5 * mid_y - 98)

def drawCard(deck, hand):
    choice = random.choice(deck.cards)
    hand.cards.append(choice)
    deck.cards.remove(choice)
    load_hand()
    updateLocations()
    return choice

def pickup_discard(hand):
    choice = discard_pile.cards[-1]
    hand.cards.append(choice)
    discard_pile.cards.remove(choice)
    load_hand()
    updateLocations()
    return choice

def discard(hand, active_card):
    hand.cards.remove(active_card)
    discard_pile.cards.append(active_card)
    load_hand()
    updateLocations()

def load_hand():
    for card in hand.cards:
        drawer.image_loader.card_images[card.name] = pygame.image.load(f'./assets/cards/{card.name}')

def get_meld_type_from_card(focus_card, melds):
    for meld in melds:
        for card in meld:
            if card == focus_card:
                if card_data[meld[0].name]["rank"] == card_data[meld[1].name]["rank"]:
                    return "set"
                else:
                    return "run"
    return "none"

def update_melds(this_hand):
    rank_groups = defaultdict(list)
    suit_groups = defaultdict(list)

    for card in this_hand.cards:
        rank = card_data[card.name]["rank"]
        suit = card_data[card.name]["suit"]
        rank_groups[rank].append(card)
        suit_groups[suit].append((rank, card))

    all_melds = []

    # sets - also generate all valid sub-sets of 3 from groups of 4
    for cards in rank_groups.values():
        if len(cards) >= 3:
            all_melds.append(cards[:])
            if len(cards) == 4:
                for i in range(4):
                    all_melds.append([c for j, c in enumerate(cards) if j != i])

    # runs - generate all valid sub-runs of length 3+
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
                        deadwood += min(card_data[card.name]["rank"], 10)
                if deadwood < best_deadwood:
                    best_deadwood = deadwood
                    best_melds = list(combo)

    return best_melds

def get_melds(card, melds):
    found_melds = []
    for meld in melds:
        if card in meld:
            found_melds.append(meld)
    return found_melds

def num_of_melds(focus_card, melds):
    cnt = 0
    for meld in melds:
        for card in meld:
            if card == focus_card:
                cnt += 1
    return cnt

def calculate_deadwood(melds, cards):
    deadwood = 0
    meld_cards = []
    for meld in melds:
        for card in meld:
            meld_cards.append(card)
    for card in cards:
        if card not in meld_cards:
            deadwood += min(card_data[card.name]["rank"], 10)

    return deadwood

def can_knock(melds, cards):
    meld_cards = []
    for meld in melds:
        for card in meld:
            meld_cards.append(card)

    greatest_deadwood = 0
    total_deadwood = 0
    for card in cards:
        if card not in meld_cards:

            if card_data[card.name]["rank"] > 10:
                total_deadwood += 10
            else:
                total_deadwood += card_data[card.name]["rank"]
            
            if card_data[card.name]["rank"] > greatest_deadwood:
                greatest_deadwood = card_data[card.name]["rank"]
    
    if total_deadwood - greatest_deadwood <= 10:
        return True
    else:
        return False

def get_greatest_deadwood(melds, cards):
    meld_cards = []
    for meld in melds:
        for card in meld:
            meld_cards.append(card)

    greatest_deadwood = 0
    gdc = None #greatest deadwood card
    total_deadwood = 0
    for card in cards:
        if card not in meld_cards:

            if card_data[card.name]["rank"] > 10:
                total_deadwood += 10
            else:
                total_deadwood += card_data[card.name]["rank"]
            
            if card_data[card.name]["rank"] > greatest_deadwood:
                greatest_deadwood = card_data[card.name]["rank"]
                gdc = card
    return gdc
    
def get_meld_type(meld):
    if card_data[meld[0].name]["rank"] == card_data[meld[1].name]["rank"]:
        return "set"
    elif (abs(card_data[meld[0].name]["rank"] - card_data[meld[1].name]["rank"]) == 1 and card_data[meld[0].name]["suit"] == card_data[meld[1].name]["suit"]):
        return "run"
    else:
        return "none"
    
def can_contribute(card, meld):
    type = get_meld_type(meld)
    if type == "run":
        if card_data[card.name]["suit"] == card_data[meld[0].name]["suit"]:
            if card_data[card.name]["rank"] == card_data[meld[0].name]["rank"] - 1:
                return True
            elif card_data[card.name]["rank"] == card_data[meld[-1].name]["rank"] + 1:
                return True
    elif type == "set":
        if card_data[card.name]["rank"] == card_data[meld[0].name]["rank"]:
            return True
    return False

def sort_cards_suit(hand):
    sort_cards_rank(hand)
    suitgroups = defaultdict(list)
    sorted_hand = []
    for card in hand.cards:
        suitgroups[card_data[card.name]["suit"]].append(card)
    
    for cards in suitgroups.values():
        for card in cards:
            sorted_hand.append(card)
    hand.cards = sorted_hand
    updateLocations()

def sort_cards_rank(hand):
    sorted_hand = []
    greatest_card = None
    while hand.cards:
        greatest_num = 0
        for card in hand.cards:
            if card_data[card.name]["rank"] >= greatest_num:
                greatest_num = card_data[card.name]["rank"]
                greatest_card = card
        hand.cards.remove(greatest_card)
        sorted_hand.append(greatest_card)
    hand.cards = sorted_hand
    updateLocations()

def calculate_round_score(knocker_hand, defender_hand):
    knocker_melds = update_melds(knocker_hand)
    defender_melds = update_melds(defender_hand)
    
    knocker_deadwood = calculate_deadwood(knocker_melds, knocker_hand.cards)
    
    # only consider cards that are actually deadwood for the defender
    defender_meld_cards = [card for meld in defender_melds for card in meld]
    defender_deadwood_cards = [card for card in defender_hand.cards if card not in defender_meld_cards]
    
    # lay off defender's deadwood onto knocker's melds
    # skip layoff entirely if knocker has gin
    laid_off = []
    if knocker_deadwood > 0:
        for meld in knocker_melds:
            for card in defender_deadwood_cards:
                if can_contribute(card, meld) and card not in laid_off:
                    laid_off.append(card)

    # calculate defender's remaining deadwood after layoffs
    defender_deadwood_score = sum(
        min(card_data[card.name]["rank"], 10)
        for card in defender_deadwood_cards
        if card not in laid_off
    )
    
    if defender_deadwood_score <= knocker_deadwood:  # undercut
        return 0, (knocker_deadwood - defender_deadwood_score) + 25
    else:
        return defender_deadwood_score - knocker_deadwood, 0

def computer_play():

    opp_hand.melds = update_melds(opp_hand)
    current_deadwood = calculate_deadwood(opp_hand.melds, opp_hand.cards)

    discard_card = discard_pile.cards[-1]
    opp_hand.cards.append(discard_card)
    simulated_melds = update_melds(opp_hand)
    simulated_deadwood = calculate_deadwood(simulated_melds, opp_hand.cards)
    opp_hand.cards.remove(discard_card)

    pickup_dis = False
    if simulated_deadwood < current_deadwood:
        opp_drawn_card = pickup_discard(opp_hand)
        pickup_dis = True
    else:
        opp_drawn_card = drawCard(deck, opp_hand)
    
    #animate card movement
    if pickup_dis:
        animate_card_flip(drawer.image_loader.card_images[opp_drawn_card.name], drawer.image_loader.blue_back, drawer.rects.discard_rect.center, (opp_drawn_card.loc[0] + 73/2, opp_drawn_card.loc[1] + 98/2), constants.CARD_MOVEMENT_SPEED, drawer.surface_loader.game_surface, opp_drawn_card, -1)
    else:
        animate_card_slide_move(drawer.image_loader.blue_back, drawer.rects.draw_rect.center, (opp_drawn_card.loc[0], opp_drawn_card.loc[1]), constants.CARD_MOVEMENT_SPEED, drawer.surface_loader.game_surface, opp_drawn_card, -1)

    #update melds after pickup
    opp_hand.melds = update_melds(opp_hand)
    
    best_discard = None
    best_deadwood = float('inf')

    for card in opp_hand.cards:
        in_meld = any(card in meld for meld in opp_hand.melds)
        if in_meld:
            continue
        
        opp_hand.cards.remove(card)
        simulated_melds = update_melds(opp_hand)
        simulated_deadwood = calculate_deadwood(simulated_melds, opp_hand.cards)
        opp_hand.cards.append(card)

        if simulated_deadwood < best_deadwood:
            best_deadwood = simulated_deadwood
            best_discard = card

    if best_discard is None:
        best_discard = opp_hand.cards[-1]

    animate_card_flip(drawer.image_loader.blue_back, drawer.image_loader.card_images[best_discard.name], (best_discard.loc[0] + 73/2, best_discard.loc[1] + 98/2), drawer.rects.discard_rect.center, constants.CARD_MOVEMENT_SPEED, drawer.surface_loader.game_surface, best_discard, -1)
    discard(opp_hand, best_discard)

    opp_hand.melds = update_melds(opp_hand)
    deadwood = calculate_deadwood(opp_hand.melds, opp_hand.cards)

    if deadwood == 0:
        opp_hand.can_knock = True
        opp_hand.can_gin = True
    elif deadwood <= 10:
        opp_hand.can_knock = True
        opp_hand.can_gin = False
    
    if opp_hand.can_gin or opp_hand.can_knock:
        global round_overlay, computer_knock
        round_overlay = True
        computer_knock = True
        opp_hand.can_knock = False
        opp_hand.can_gin = False
    
    #return hamburger_x

def show_start_screen():
    #moving background
    x_offset = 0.0
    background_clock = pygame.time.Clock()
    animating = False
    anim_frames = 60
    frame = 0
    singleplayer = True

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  #start game on enter key
                    animating = True
                elif event.key == pygame.K_LSHIFT:
                    animating = True
                    singleplayer = False
                    

        x_offset -= 0.5
        if x_offset <= -drawer.image_loader.title_background_width:
            x_offset = 0
        # # # screen.display_surface.blit(drawer.image_loader.title_background, (int(x_offset), 0))
        # # # screen.display_surface.blit(drawer.image_loader.title_background, (int(x_offset + drawer.image_loader.title_background_width), 0))

        if animating and frame < anim_frames:
            drawer.text_renderer.update_title(frame, anim_frames)
            #text_alpha = (255 * (1 - exponential))
            frame += 2
        elif animating and frame >= anim_frames: #continues to scroll the background after the title fades
            for i in range(15): #waits 15 frames
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                
                x_offset -= 0.5
                if x_offset <= -drawer.image_loader.title_background_width:
                    x_offset = 0

                # # # screen.display_surface.blit(drawer.image_loader.title_background, (int(x_offset), 0))
                # # # screen.display_surface.blit(drawer.image_loader.title_background, (int(x_offset + drawer.image_loader.title_background_width), 0))
                # # # screen.display_surface.blit(drawer.text_renderer.start_text, drawer.rects.start_rect)
                # # # screen.display_surface.blit(drawer.text_renderer.multiplayer_text, drawer.rects.multiplayer_rect)

                pygame.display.flip()
                background_clock.tick(200)

            waiting = False

        #title_font = pygame.font.Font('./assets/fonts/Mermaid1001.ttf', round(title_size))
        #title_text = text_renderer.title_font.render("Gin Rummy", True, (255,222,133))
        #text_renderer.set_alpha(text_renderer.title_text, text_alpha)
        title_rect = drawer.text_renderer.title_text.get_rect(center=(screen.display_width / 2, screen.display_height * 5/12))
        # # # screen.display_surface.blit(drawer.text_renderer.title_text, title_rect)
        screen.display_surface.blit(drawer.text_renderer.start_text, drawer.rects.start_rect)
        screen.display_surface.blit(drawer.text_renderer.multiplayer_text, drawer.rects.multiplayer_rect)

        pygame.display.flip()
        background_clock.tick(200)
    return x_offset, singleplayer

# def update_menu_rects():
#     global r_option_rect, mm_option_rect, c_option_rect, s_option_rect, qg_option_rect

#     option_width = screen.display_width / 10
#     option_height = screen.display_height / 15
#     option_left = screen.menu_x + screen.menu_width / 2 - option_width / 2
#     option_top = screen.display_height / 11

#     r_option_rect = pygame.Rect(option_left, option_top, option_width, option_height)
#     mm_option_rect = pygame.Rect(option_left, option_top * 2, option_width, option_height)
#     c_option_rect = pygame.Rect(option_left, option_top * 3, option_width, option_height)
#     s_option_rect = pygame.Rect(option_left, option_top * 4, option_width, option_height)
#     qg_option_rect = pygame.Rect(option_left, option_top * 5, option_width, option_height)

#drawing functions
#def draw_game_screen(menu_x, hamburger_x, surface):
def draw_game_screen(): #maybe change to create game screen later
    draw_background(drawer.surface_loader.game_surface)
    drawer.draw_menu(drawer.surface_loader.game_surface, menu_active, dt)
    draw_buttons(drawer.surface_loader.game_surface)
    draw_cards(drawer.surface_loader.game_surface)
    screen.display_surface.blit(drawer.surface_loader.game_surface, (0,0))

def draw_background(surface):
    surface.blit(drawer.image_loader.background, (0,0))

def draw_networking_screen(dt):
    drawer.surface_loader.networking_surface.blit(drawer.image_loader.networking_background, (0,0))
    drawer.surface_loader.networking_surface.blit(drawer.text_renderer.multiplayer_menu_text, drawer.rects.multiplayer_menu_rect)
    animator.animate_loading(dt, drawer.surface_loader.networking_surface)
    drawer.draw_menu(drawer.surface_loader.networking_surface, menu_active, dt)
    screen.display_surface.blit(drawer.surface_loader.networking_surface, (0,0))

def draw_cards(surface):

    #draw pile
    surface.blit(drawer.image_loader.blue_back, (surface.get_width() * 4/9 - constants.CARD_WIDTH / 2, surface.get_height() / 2 - constants.CARD_HEIGHT / 2))

    #outline when discard pile is empty
    pygame.draw.rect(surface, "white", pygame.Rect(surface.get_width() * 5/9 - constants.CARD_WIDTH / 2, surface.get_height() / 2 - constants.CARD_HEIGHT / 2, 73, 98), 4, border_radius=10)
    
    #drawing the opponents hand
    for card in opp_hand.cards:
        if card.visible:
            #surface.blit(blue_back, card.loc)
            surface.blit(drawer.image_loader.card_images[card.name], card.loc)

    #discard pile
    if discard_pile.cards:
        if len(discard_pile.cards) > 1:
            #discard_top = pygame.image.load(f'./assets/cards/{discard_pile.cards[len(discard_pile.cards) - 2].name}')
            discard_top = drawer.image_loader.card_images[discard_pile.cards[-2].name]
            surface.blit(discard_top, (surface.get_width() * 5/9 - constants.CARD_WIDTH / 2, surface.get_height() / 2 - constants.CARD_HEIGHT / 2))
        if discard_pile.cards[-1].visible:
            #discard_top = pygame.image.load(f'./assets/cards/{discard_pile.cards[-1].name}')
            discard_top = drawer.image_loader.card_images[discard_pile.cards[-1].name]
            surface.blit(discard_top, (surface.get_width() * 5/9 - constants.CARD_WIDTH / 2, surface.get_height() / 2 - constants.CARD_HEIGHT / 2))

    #drawing the hand while you're holding a card
    if active_card:
        active_card_x = active_card.loc[0]
        for card in hand.cards:
            if card.loc[0] < active_card_x: #draw all the card before the active card first
                surface.blit(drawer.image_loader.card_images[card.name], (card.loc))
        surface.blit(drawer.image_loader.card_images[active_card.name], (active_card.loc)) #draw the active card
        for card in hand.cards:
            if card.loc[0] > active_card_x: #draw all the cards after the active card last
                surface.blit(drawer.image_loader.card_images[card.name], (card.loc))
    else:
        for card in hand.cards:
            if card.visible:
                surface.blit(drawer.image_loader.card_images[card.name], (card.loc))
         
#def draw_menu(menu_x, hamburger_x, surface):
# def draw_menu(surface):
#     if menu_active: #opening the menu
#         #hamburger_tx = -1.5 * hamburger_width
#         screen.hamburger_x = max(screen.hamburger_x - (constants.MENU_SPEED * dt), -1.5 * constants.HAMBURGER_WIDTH) #moves the hamburger from the other value to x=-1.5 * hamburger_width
#         screen.menu_x = min(screen.menu_x + (constants.MENU_SPEED * dt), 0)
#         drawer.rects.update_option_rects()
#         #surface.blit(side_overlay, (menu_x, 0))
#         surface.blit(drawer.surface_loader.side_overlay, (screen.menu_x, 0))
#         #option_width = screen.display_width/10
#         #option_height = screen.display_height/15
#         #option_left = menu_x + screen.menu_width/2 - option_width/2
#         #option_top = screen.display_height/11
#         #r_option_rect = pygame.Rect(option_left, option_top, option_width, option_height) #retry option
#         #r_option_text = medium_font.render("Retry", True, WHITE)
#         #mm_option_rect = pygame.Rect(option_left, option_top*2, option_width, option_height) #main menu option
#         #mm_option_text = medium_font.render("Main Menu", True, WHITE)
#         #c_option_rect = pygame.Rect(option_left, option_top*3, option_width, option_height) #customize option
#         #c_option_text = medium_font.render("Customize", True, WHITE)
#         #s_option_rect = pygame.Rect(option_left, option_top*4, option_width, option_height) #settings option
#         #s_option_text = medium_font.render("Settings", True, WHITE)
#         #qg_option_rect = pygame.Rect(option_left, option_top*5, option_width, option_height) #quit game option
#         #qg_option_text = medium_font.render("Quit Game", True, WHITE)
#         surface.blit(drawer.text_renderer.r_option_text, drawer.text_renderer.r_option_text.get_rect(center=drawer.rects.r_option_rect.center)) #retry option
#         surface.blit(drawer.text_renderer.mm_option_text, drawer.text_renderer.mm_option_text.get_rect(center=drawer.rects.mm_option_rect.center)) #main menu option
#         surface.blit(drawer.text_renderer.c_option_text, drawer.text_renderer.c_option_text.get_rect(center=drawer.rects.c_option_rect.center)) #customize option
#         surface.blit(drawer.text_renderer.s_option_text, drawer.text_renderer.s_option_text.get_rect(center=drawer.rects.s_option_rect.center)) #settings option
#         surface.blit(drawer.text_renderer.qg_option_text, drawer.text_renderer.qg_option_text.get_rect(center=drawer.rects.qg_option_rect.center)) #quit game option

#     else: #closing the menu

#         surface.blit(drawer.surface_loader.side_overlay, (screen.menu_x, 0))
#         screen.hamburger_x = min(screen.hamburger_x + (constants.MENU_SPEED * dt), 30) #moves the hamburger from x=30 to the other value
#         screen.menu_x = max(screen.menu_x - (constants.MENU_SPEED * dt), -1.5 * screen.menu_width)
#         drawer.rects.update_option_rects()

#         surface.blit(drawer.text_renderer.r_option_text, drawer.text_renderer.r_option_text.get_rect(center=drawer.rects.r_option_rect.center)) #retry option
#         surface.blit(drawer.text_renderer.mm_option_text, drawer.text_renderer.mm_option_text.get_rect(center=drawer.rects.mm_option_rect.center)) #main menu option
#         surface.blit(drawer.text_renderer.c_option_text, drawer.text_renderer.c_option_text.get_rect(center=drawer.rects.c_option_rect.center)) #customize option
#         surface.blit(drawer.text_renderer.s_option_text, drawer.text_renderer.s_option_text.get_rect(center=drawer.rects.s_option_rect.center)) #settings option
#         surface.blit(drawer.text_renderer.qg_option_text, drawer.text_renderer.qg_option_text.get_rect(center=drawer.rects.qg_option_rect.center)) #quit game option

#     #menu icon
#     pygame.draw.rect(surface, "white", pygame.Rect(screen.hamburger_x,30,constants.HAMBURGER_WIDTH,8))
#     pygame.draw.rect(surface, "white", pygame.Rect(screen.hamburger_x,45,constants.HAMBURGER_WIDTH,8))
#     pygame.draw.rect(surface, "white", pygame.Rect(screen.hamburger_x,60,constants.HAMBURGER_WIDTH,8))

    ##return hamburger_x

def draw_buttons(surface):
    pygame.draw.rect(surface, (200, 200, 200), drawer.rects.sort_rect_rank, border_radius=8)
    pygame.draw.rect(surface, constants.BLACK, drawer.rects.sort_rect_rank, 2, border_radius=8)
    pygame.draw.rect(surface, (200, 200, 200), drawer.rects.sort_rect_suit, border_radius=8)
    pygame.draw.rect(surface, constants.BLACK, drawer.rects.sort_rect_suit, 2, border_radius=8)
    surface.blit(drawer.text_renderer.sort_rank_text, drawer.text_renderer.sort_rank_text.get_rect(center=drawer.rects.sort_rect_rank.center))
    surface.blit(drawer.text_renderer.sort_suit_text, drawer.text_renderer.sort_suit_text.get_rect(center=drawer.rects.sort_rect_suit.center))

    #player knock button
    if hand.can_knock:
        pygame.draw.rect(surface, (200, 200, 200), drawer.rects.player_knock_rect, border_radius=8)
        pygame.draw.rect(surface, constants.BLACK, drawer.rects.player_knock_rect, 2, border_radius=8)
        surface.blit(drawer.text_renderer.player_knock_text, drawer.text_renderer.player_knock_text.get_rect(center=drawer.rects.player_knock_rect.center))

    #opponent knock button
    if opp_hand.can_knock:
        pygame.draw.rect(surface, (200, 200, 200), drawer.rects.opp_knock_rect, border_radius=8)
        pygame.draw.rect(surface, constants.BLACK, drawer.rects.opp_knock_rect, 2, border_radius=8)
        surface.blit(drawer.text_renderer.opp_knock_text, drawer.text_renderer.opp_knock_text.get_rect(center=drawer.rects.opp_knock_rect.center))

def animate_card_flip(back_img, front_img, start_pos, end_pos, duration, surface, card, turn):
    if turn == 1:
        card.visible = False
    frame_count = int(duration / (1000 / 60))
    for frame in range(frame_count):
        progress = frame / frame_count
        progress_eased = 1 - (1 - progress) ** 3

        x = start_pos[0] + (end_pos[0] - start_pos[0]) * progress_eased #moves closer to the end_pos using the difference
        y = start_pos[1] + (end_pos[1] - start_pos[1]) * progress_eased

        if progress < 0.5:
            scale = 1 - (2 * progress) #shrinks until it reaches 0
            image = back_img
        else:
            scale = 2 * (progress - 0.5) #grows until it reaches 1
            image = front_img
        
        scaled_width = max(1, int(image.get_width() * scale)) #scales the width until it reaches 100%
        scaled_image = pygame.transform.scale(image, (scaled_width, image.get_height()))

        draw_x = int(x - scaled_width // 2)
        draw_y = int(y - image.get_height() // 2)

        draw_background(surface)
        draw_buttons(surface)
        if turn == 1:
            draw_cards(surface)
            surface.blit(scaled_image, (draw_x, draw_y))
        else: #opp turn

            #draw pile
            surface.blit(drawer.image_loader.blue_back, (surface.get_width() * 4/9 - constants.CARD_WIDTH / 2, surface.get_height() / 2 - constants.CARD_HEIGHT / 2))

            #outline when discard pile is empty
            pygame.draw.rect(surface, "white", pygame.Rect(surface.get_width() * 5/9 - constants.CARD_WIDTH / 2, surface.get_height() / 2 - constants.CARD_HEIGHT / 2, 73, 98), 4, border_radius=10)

            #discard pile
            if discard_pile.cards:
                if len(discard_pile.cards) > 1:
                    #discard_top = pygame.image.load(f'./assets/cards/{discard_pile.cards[len(discard_pile.cards) - 2].name}')
                    discard_top = drawer.image_loader.card_images[discard_pile.cards[-2].name]
                    surface.blit(discard_top, (surface.get_width() * 5/9 - constants.CARD_WIDTH / 2, surface.get_height() / 2 - constants.CARD_HEIGHT / 2))
                if discard_pile.cards[-1].visible:
                    #discard_top = pygame.image.load(f'./assets/cards/{discard_pile.cards[-1].name}')
                    discard_top = drawer.image_loader.card_images[discard_pile.cards[-1].name]
                    surface.blit(discard_top, (surface.get_width() * 5/9 - constants.CARD_WIDTH / 2, surface.get_height() / 2 - constants.CARD_HEIGHT / 2))

            index = opp_hand.cards.index(card)
            for i in range(index):#cards before
                surface.blit(drawer.image_loader.blue_back, opp_hand.cards[i].loc)
            if card.visible: #animated card
                surface.blit(scaled_image, (draw_x, draw_y))
            for i in range(index + 1, len(opp_hand.cards)): #cards after
                surface.blit(drawer.image_loader.blue_back, opp_hand.cards[i].loc)
            for player_card in hand.cards: #player hand
                surface.blit(drawer.image_loader.card_images[player_card.name], player_card.loc)
        
        drawer.draw_menu(surface, menu_active, dt)
        screen.display_surface.blit(surface, (0,0))
        pygame.display.flip()
    card.visible = True
    #return hamburger_x  

def animate_card_slide_move(front_img, start_pos, end_pos, duration, surface, card, turn):
    if turn == 1:
        card.visible = False
    frame_count = int(duration / (1000 / 60))
    for frame in range(frame_count):
        progress = frame / frame_count
        progress_eased = 1 - (1 - progress) ** 3

        x = start_pos[0] + (end_pos[0] - start_pos[0]) * progress_eased #moves closer to the end_pos using the difference
        y = start_pos[1] + (end_pos[1] - start_pos[1]) * progress_eased

        draw_background(surface)
        draw_buttons(surface)
        if turn == 1:
            draw_cards(surface)
            surface.blit(front_img, (x, y))
        else: #opp turn
            
            #draw pile
            surface.blit(drawer.image_loader.blue_back, (surface.get_width() * 4/9 - constants.CARD_WIDTH / 2, surface.get_height() / 2 - constants.CARD_HEIGHT / 2))

            #outline when discard pile is empty
            pygame.draw.rect(surface, "white", pygame.Rect(surface.get_width() * 5/9 - constants.CARD_WIDTH / 2, surface.get_height() / 2 - constants.CARD_HEIGHT / 2, 73, 98), 4, border_radius=10)

            #discard pile
            if discard_pile.cards:
                if len(discard_pile.cards) > 1:
                    #discard_top = pygame.image.load(f'./assets/cards/{discard_pile.cards[len(discard_pile.cards) - 2].name}')
                    discard_top = drawer.image_loader.card_images[discard_pile.cards[-2].name]
                    surface.blit(discard_top, (surface.get_width() * 5/9 - constants.CARD_WIDTH / 2, surface.get_height() / 2 - constants.CARD_HEIGHT / 2))
                if discard_pile.cards[-1].visible:
                    #discard_top = pygame.image.load(f'./assets/cards/{discard_pile.cards[-1].name}')
                    discard_top = drawer.image_loader.card_images[discard_pile.cards[-1].name]
                    surface.blit(discard_top, (surface.get_width() * 5/9 - constants.CARD_WIDTH / 2, surface.get_height() / 2 - constants.CARD_HEIGHT / 2))

            index = opp_hand.cards.index(card)
            for i in range(index):#cards before
                surface.blit(drawer.image_loader.blue_back, opp_hand.cards[i].loc)
            if card.visible: #animated card
                surface.blit(drawer.image_loader.blue_back, (x, y))
            for i in range(index + 1, len(opp_hand.cards)): #cards after
                surface.blit(drawer.image_loader.blue_back, opp_hand.cards[i].loc)
            for player_card in hand.cards: #player hand
                surface.blit(drawer.image_loader.card_images[player_card.name], player_card.loc)
        
        drawer.draw_menu(surface, menu_active, dt)
        screen.display_surface.blit(surface, (0,0))
        pygame.display.flip()
    card.visible = True
    #return hamburger_x 

def update_title_background(test):
    test -= dt
    if test <= -drawer.image_loader.title_background_width:
        test = 0

    screen.display_surface.blit(drawer.image_loader.title_background, (int(test), 0))
    screen.display_surface.blit(drawer.image_loader.title_background, (int(test + drawer.image_loader.title_background_width), 0))  
    screen.display_surface.blit(drawer.text_renderer.start_text, drawer.rects.start_rect)
    screen.display_surface.blit(drawer.text_renderer.multiplayer_text, drawer.rects.multiplayer_rect)

updateLocations()
sort_cards_rank(opp_hand)
load_hand()
x_offset, singleplayer = show_start_screen() #menu starts here and waits for enter or shift
mixer.shuffle_sound.play()



#shows the screen wipe
# if singleplayer and not animator.title_wipe.finished:
#     draw_game_screen()
#     #animator.animate_title_wipe(dt, drawer.surface_loader.game_surface)
#     test = 0
#     for wipe_x in range(0, screen.display_width + 1, constants.TITLE_WIPE_SPEED):
#         #update_title_background(test)
#         #update_title_background(x_offset)
#         #x_offset -= 0.5
#         #screen.display_surface.blit(drawer.surface_loader.game_surface, (0, 0), area=pygame.Rect(0, 0, wipe_x, screen.display_height))
#         pygame.display.flip()
#         clock.tick(200)

while running:
    dt = clock.tick(200) / 1000 #fps 

    if singleplayer and not animator.title_wipe.finished:
        draw_game_screen()
        animator.animate_title_background(dt, drawer.surface_loader.game_surface)
        animator.animate_title_wipe(dt, drawer.surface_loader.game_surface)


#COME BACK TO THIS AFTER FINISHING THE TITLE WIPE



    # else: #else multiplayer:

    #     draw_networking_screen(dt)
    #     for wipe_x in range(screen.display_width, -1, -constants.TITLE_WIPE_SPEED):
    #         update_title_background(x_offset)
    #         x_offset -= 0.5
    #         screen.display_surface.blit(drawer.surface_loader.networking_surface, (0,0), area=pygame.Rect(-wipe_x, 0, screen.display_width, screen.display_height))
    #         pygame.display.flip()
    #         clock.tick(200)

    #     mixer.start_networking_music()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_RETURN:
                
                if round_overlay:
                    if hand.score >= 100 or opp_hand.score >= 100:
                        print("game over")
                    else:
                        # save scores
                        saved_player_score = hand.score
                        saved_opp_score = opp_hand.score
                        
                        # reset everything
                        deck = Deck()
                        hand = Hand(deck)
                        discard_pile = DiscardPile(deck)
                        opp_hand = Hand(deck)
                        
                        # restore scores
                        hand.score = saved_player_score
                        opp_hand.score = saved_opp_score
                        
                        # reset round state
                        round_overlay = False
                        player_knock = False
                        computer_knock = False
                        knocking = False
                        turn = 1
                        player_turn = 1
                        drawer.text_renderer.player_score_text = None
                        drawer.text_renderer.opp_score_text = None
                        
                        updateLocations()
                        sort_cards_rank(opp_hand)
                        load_hand()
                        horizontal_shift = (((screen.display_surface.get_width() / 3) / len(hand.cards)) * 0.8)



        #game mouse detection singleplayer
        if singleplayer:
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    
                    if drawer.rects.menu_rect.collidepoint(event.pos):
                        menu_active = True

                    if drawer.rects.main_menu_overlay_rect.collidepoint(event.pos): #close the menu if it's open and you click off
                        menu_active = False
                    
                    if menu_active: #menu options
                        drawer.rects.update_option_rects()
                        if drawer.rects.mm_option_rect.collidepoint(event.pos):
                            restart_from_main_menu = True
                        if drawer.rects.qg_option_rect.collidepoint(event.pos):
                            running = False
                        if drawer.rects.r_option_rect.collidepoint(event.pos):
                            restart = True

                    #game interactions start here
                    for card in reversed(hand.cards):
                        if card == hand.cards[-1]:      #if card is on the right, it's rect is larger
                            card_rect = pygame.Rect(card.loc[0], card.loc[1], 73, 98)
                        else:                           #else we need to modify the rect to match the size
                            card_rect = pygame.Rect(card.loc[0], card.loc[1], ((screen.display_surface.get_width() / 3) / (len(hand.cards) - 1)) * 0.8, 98)

                        if card_rect.collidepoint(event.pos): #if mousedown on a card rect
                            clicked = True
                            active_card = card
                            active_card.dragging = True
                            original_loc = active_card.loc
                            original_index = hand.cards.index(active_card)
                            card_x = event.pos[0] - active_card.loc[0]
                            card_y = event.pos[1] - active_card.loc[1]
                            break
                        elif drawer.rects.draw_rect.collidepoint(event.pos):
                            if turn == 1:
                                random.choice(mixer.thwip_sounds).play()
                                drawn_card = drawCard(deck, hand)
                                animate_card_flip(drawer.image_loader.blue_back, drawer.image_loader.card_images[drawn_card.name], drawer.rects.draw_rect.center, (hand.cards[-1].loc[0] + 73/2, hand.cards[-1].loc[1] + 98/2), constants.CARD_MOVEMENT_SPEED, drawer.surface_loader.game_surface, drawn_card, turn)
                                drawn_card = None
                                horizontal_shift = (((screen.display_surface.get_width() / 3) / len(hand.cards)) * 0.8)
                                hand.melds = update_melds(hand)
                                if can_knock(hand.melds, hand.cards):
                                    hand.can_knock = True
                                turn *= -1
                                break
                        elif drawer.rects.discard_rect.collidepoint(event.pos):
                            if turn == 1:
                                mixer.slide_sound.play()
                                drawn_card = pickup_discard(hand)
                                animate_card_slide_move(drawer.image_loader.card_images[drawn_card.name], drawer.rects.discard_rect.center, (hand.cards[-1].loc[0], hand.cards[-1].loc[1]), constants.CARD_MOVEMENT_SPEED, drawer.surface_loader.game_surface, drawn_card, turn)
                                drawn_card = None
                                horizontal_shift = (((screen.display_surface.get_width() / 3) / len(hand.cards)) * 0.8)
                                hand.melds = update_melds(hand)
                                if can_knock(hand.melds, hand.cards):
                                    hand.can_knock = True
                                #if discard_pile.cards:
                                #    discard_top = pygame.image.load(f'./assets/cards/{discard_pile.cards[-1].name}')
                                #    discard_top = card_images[discard_pile.cards[-1].name]
                                #    pass
                                turn *= -1
                                break
                        elif drawer.rects.sort_rect_rank.collidepoint(event.pos):
                            sort_cards_rank(hand)
                        elif drawer.rects.sort_rect_suit.collidepoint(event.pos):
                            sort_cards_suit(hand)
                        elif drawer.rects.player_knock_rect.collidepoint(event.pos):
                            knocking = True

            elif event.type == pygame.MOUSEMOTION and clicked == True:
                if active_card:
                    active_card.loc = (event.pos[0] - card_x, event.pos[1] - card_y)

            elif event.type == pygame.MOUSEMOTION:
                pass

            elif event.type == pygame.MOUSEBUTTONUP:

                if active_card:
                    active_card.dragging = False

                    shi = None #starting hover index

                    if original_loc[0] > active_card.loc[0]: #if you moved the active card to the left
                        for i, card in enumerate(hand.cards):
                            if card.hovered_x and card is not active_card:
                                shi = i
                                break
                        if shi is None:
                            shi = original_index
                        placeholder = active_card
                        for i in range(original_index, shi, -1):
                            hand.cards[i] = hand.cards[i-1]
                        hand.cards[shi] = placeholder

                    elif original_loc[0] < active_card.loc[0]: #if you moved the active card to the right
                        for i in range(len(hand.cards)-1, -1, -1):
                            if hand.cards[i].hovered_x and hand.cards[i] != active_card:
                                shi = i
                                break
                        if shi is None:
                            shi = original_index
                        placeholder = active_card
                        for i in range(original_index, shi, 1):
                            hand.cards[i] = hand.cards[i+1]
                        hand.cards[shi] = placeholder

                    if drawer.rects.discard_rect.collidepoint(event.pos) and turn == -1:
                        discard(hand, active_card)
                        horizontal_shift = (((screen.display_surface.get_width() / 3) / len(hand.cards)) * 0.8)
                        #discard_top = pygame.image.load(f'./assets/cards/{discard_pile.cards[-1].name}')


                        #discard_top = card_images[discard_pile.cards[-1].name]

                        if knocking:
                            round_overlay = True
                            player_knock = True
                            knocking = False
                        else:
                            turn *= -1
                            player_turn *= -1

                    updateLocations()

                    for card in hand.cards:
                        card.hovered_x = False

                    active_card = None
                    clicked = False
        else: #multiplayer

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if drawer.rects.menu_rect.collidepoint(event.pos):
                        menu_active = True

                    if drawer.rects.main_menu_overlay_rect.collidepoint(event.pos): #close the menu if it's open and you click off
                        menu_active = False
                    
                    if menu_active: #menu options
                        drawer.rects.update_option_rects()
                        if drawer.rects.mm_option_rect.collidepoint(event.pos):
                            restart_from_main_menu = True
                        if drawer.rects.qg_option_rect.collidepoint(event.pos):
                            running = False
                        if drawer.rects.r_option_rect.collidepoint(event.pos):
                            restart = True

    #hover_y logic
    mouse_x, mouse_y = pygame.mouse.get_pos()
    hover_candidate_y = None

    for card in reversed(hand.cards):
        if card.dragging:
            continue
        width = 73 if card == hand.cards[-1] else (screen.display_surface.get_width() / 3) / max(len(hand.cards) - 1, 1) * 0.8
        rect = pygame.Rect(card.loc[0], card.base_y, width, 98)
        if rect.collidepoint((mouse_x, mouse_y)):
            hover_candidate_y = card
            break

    for card in hand.cards:
        if card is hover_candidate_y and not clicked:
            card.hovered_y = True
            card.target_y = card.base_y - card.vertical_offset
        elif card is hover_candidate_y and clicked and active_card:
            pass
        else:
            card.hovered_y = False
            card.target_y = card.base_y

    for card in hand.cards:
        if card.dragging:
            continue
        x, y = card.loc
        target = card.target_y 
        distance = target - y
        card.velocity_y += distance * 0.2
        card.velocity_y *= 0.35
        y += card.velocity_y

        if abs(distance) < 0.5 and abs(card.velocity_y) < 0.5:
            y = target
            card.velocity_y = 0

        card.loc = (x, y) #update the card location

    #hover_x logic
    if active_card:
        for i, card in enumerate(hand.cards):
            if card.dragging:
                continue
            if card.loc[0] > active_card.loc[0] and i < original_index and card != active_card: #moving active card to the left
                card.hovered_x = True
                card.target_x = card.base_x + horizontal_shift

            elif card.loc[0] < active_card.loc[0] and i > original_index and card != active_card: #moving active card to the right
                card.hovered_x = True
                card.target_x = card.base_x - horizontal_shift

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


    #---------------------------------------Drawing Starts Here---------------------------------------#

    if singleplayer:
        # draw_background(screen.display_surface)
        # draw_menu(screen.display_surface)
        # draw_buttons(screen.display_surface)
        # draw_cards(screen.display_surface)
        draw_game_screen()
    else:
        #draw_networking_background(screen.display_surface)
        #draw_menu(screen.display_surface)
        #screen.display_surface.blit(drawer.text_renderer.multiplayer_menu_text, drawer.rects.multiplayer_menu_rect)
        draw_networking_screen(dt)
    #round overlay
    if round_overlay:
        overlay = pygame.Surface(screen.display_surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        screen.display_surface.blit(overlay, (0, 0))


        if player_knock or computer_knock:
            hand.melds = update_melds(hand)
            opp_hand.melds = update_melds(opp_hand)
    
            if player_knock:    #player knock logic
                player_score, opp_score = calculate_round_score(hand, opp_hand)
                hand.score += player_score
                opp_hand.score += opp_score
                player_knock = False

            else:               #computer knock logic
                opp_score, player_score = calculate_round_score(opp_hand, hand)
                hand.score += player_score
                opp_hand.score += opp_score
                computer_knock = False

            drawer.text_renderer.update_score_text(hand.score, opp_hand.score)


        if drawer.text_renderer.player_score_text and drawer.text_renderer.opp_score_text:
            screen.display_surface.blit(drawer.text_renderer.continue_text, drawer.text_renderer.continue_text.get_rect(center=(screen.display_width // 2, screen.display_height * 2/3)))
            screen.display_surface.blit(drawer.text_renderer.player_score_text, drawer.text_renderer.player_score_text.get_rect(center=(screen.display_width // 2, screen.display_height * 1/3)))
            screen.display_surface.blit(drawer.text_renderer.opp_score_text, drawer.text_renderer.opp_score_text.get_rect(center=(screen.display_width // 2, (screen.display_height * 1/3) + 25)))
    
    #advance the turn
    if (player_turn == -1):
        computer_play()
        sort_cards_rank(opp_hand)
        #discard_top = pygame.image.load(f'./assets/cards/{discard_pile.cards[-1].name}')
        #discard_top = card_images[discard_pile.cards[-1].name]
        player_turn *= -1

    #restart from title screen
    if restart_from_main_menu:
        menu_active = False
        screen.menu_x = -1.5 * screen.menu_width
        screen.hamburger_x = 30
        turn = 1
        drawer.text_renderer = TextRenderer()
        deck = Deck()
        hand = Hand(deck)
        discard_pile = DiscardPile(deck)
        opp_hand = Hand(deck)
        updateLocations()
        sort_cards_rank(opp_hand)
        load_hand()
        x_offset, singleplayer = show_start_screen()
        mixer.shuffle_sound.play()

        #shows the screen wipe
        if singleplayer:
            draw_game_screen()
            #draw_game_screen(screen.display_surface)
            for wipe_x in range(0, screen.display_width + 1, constants.TITLE_WIPE_SPEED):
                update_title_background(x_offset)
                x_offset -= 0.5
                screen.display_surface.blit(drawer.surface_loader.game_surface, (0, 0), area=pygame.Rect(0, 0, wipe_x, screen.display_height))
                pygame.display.flip()
                clock.tick(200)
        else:
            draw_networking_screen(dt)
            for wipe_x in range(screen.display_width, -1, -constants.TITLE_WIPE_SPEED):
                update_title_background(x_offset)
                x_offset -= 0.5
                screen.display_surface.blit(drawer.surface_loader.networking_surface, (0,0), area=pygame.Rect(-wipe_x, 0, screen.display_width, screen.display_height))
                pygame.display.flip()
                clock.tick(200)

        restart_from_main_menu = False

    #restart from game
    if restart:
        menu_active = False
        turn = 1
        deck = Deck()
        hand = Hand(deck)
        discard_pile = DiscardPile(deck)
        opp_hand = Hand(deck)
        updateLocations()
        draw_cards(drawer.surface_loader.game_surface)
        load_hand()
        restart = False

    pygame.display.flip()

pygame.quit()