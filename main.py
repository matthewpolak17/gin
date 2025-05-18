
#--------- Glossary ---------
# [WIP] -> Work in Progress
# [RL]  -> Remove Later
# [DB]  -> Debugging

import pygame
import random
import csv
import os
from screeninfo import get_monitors
from collections import defaultdict
from deck import Deck
from hand import Hand
from discard_pile import DiscardPile

#game displays on second monitor for debugging
monitors = get_monitors()
second_monitor = monitors[1]
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{second_monitor.x},{second_monitor.y}"

#screen setup
pygame.init()
info = pygame.display.Info()
native_width, native_height = info.current_w, info.current_h
flags = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
display_surface = pygame.display.set_mode((native_width, native_height), flags)
pygame.display.set_caption("Gin Rummy")
clock = pygame.time.Clock()
displayHeight = native_height
displayWidth = native_width

#game variables
running = True
dropped = False
clicked = False
round_overlay = False
player_knock = False
computer_knock = False
deck = Deck()
hand = Hand(deck)
discard_pile = DiscardPile(deck)
opp_hand = Hand(deck)
original_loc = (0, 0)
horizontal_shift = (((display_surface.get_width() / 3) / len(hand.cards)) * 0.8) #determines how far to hover cards horizontally
discard_top = None
active_card = None
card_images = {}
card_data = {}
dt = 0
original_index = None
turn = 1
player_turn = 1
restart_from_main_menu = False
large_font = pygame.font.Font(None, 50)
medium_font = pygame.font.Font(None, 35)
small_font = pygame.font.Font(None, 30)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#menu variables
hamburger_x = 30
hamburger_width = 50
hamburger_tx = -1.5 * hamburger_width

menu_rect = pygame.Rect(20,20,70,58)
menu_width = display_surface.get_width() / 4
menu_x = -1.5 * menu_width
menu_tx = 0
menu_speed = 2600
menu_overlay = False
main_menu_overlay_rect = pygame.Rect(menu_width, 0, display_surface.get_width() - menu_width, displayHeight)

side_overlay = pygame.Surface((menu_width, displayHeight), pygame.SRCALPHA)
side_overlay.fill((0, 0, 0,  80))

#sorting buttons
sort_rect_rank = pygame.Rect(displayWidth * 2/3, displayHeight * 0.75, 80, 40)
sort_rect_suit = pygame.Rect(displayWidth * 2/3, displayHeight * 0.8, 80, 40)
sort_rank_text = small_font.render("Rank", True, BLACK)
sort_suit_text = small_font.render("Suit", True, BLACK)
sort_rank_rect = sort_rank_text.get_rect(center=sort_rect_rank.center)
sort_suit_rect = sort_suit_text.get_rect(center=sort_rect_suit.center)

#knocking buttons
player_knock_rect = pygame.Rect(displayWidth * 2/3, displayHeight * 0.70, 80, 40)
opp_knock_rect = pygame.Rect(displayWidth * 2/3, displayHeight * 0.2, 80, 40)
player_knock_text = small_font.render("Knock", True, BLACK)
opp_knock_text = small_font.render("Knock", True, BLACK)
knock_player_rect = player_knock_text.get_rect(center=player_knock_rect.center)
knock_opp_rect = opp_knock_text.get_rect(center=opp_knock_rect.center)

#images loaded here
discard_top = pygame.image.load(f'gin/assets/cards/{discard_pile.cards[-1].name}')
icon = pygame.image.load(f'gin/assets/icon.png').convert_alpha()
background = pygame.image.load(r'gin/assets/background.png').convert_alpha()
background = pygame.transform.scale(background, (native_width, native_height))
blue_back = pygame.transform.scale(pygame.image.load(r'gin/assets/blueback.png'), (73, 98))
pygame.display.set_icon(icon)

#card_data is filled here
with open('gin/assets/card_values.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        card_data[row['name']] = {'suit': row['suit'], 'rank': int(row['rank'])}

#rects
draw_rect = pygame.Rect(display_surface.get_width() * 4/9 - blue_back.get_width() / 2, display_surface.get_height() / 2 - blue_back.get_height() / 2, 73, 98)
knock_rect = pygame.Rect(display_surface.get_width() - 60, display_surface.get_height() - 30, 30, 10)
opp_knock_rect = pygame.Rect(display_surface.get_width() - 60, display_surface.get_height() - 90, 30, 10)
discard_rect = pygame.Rect(display_surface.get_width() * 5/9 - blue_back.get_width() / 2, display_surface.get_height() / 2 - blue_back.get_height() / 2, 73, 98)

def load_card_images():
    images = {}
    for name in card_data:
        img = pygame.image.load(f'gin/assets/cards/{name}').convert_alpha()
        images[name] = pygame.transform.smoothscale(img, (73, 98))
    return images

card_images = load_card_images()

#functions
def updateLocations():
    def set_card_positions(cards, y_offset, spacing_scale=0.8):
        win_width = display_surface.get_width()
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

    mid_y = display_surface.get_height() / 2
    set_card_positions(hand.cards, 1.5 * mid_y)
    set_card_positions(opp_hand.cards, 0.5 * mid_y - 98)

def drawCard(deck, hand):
    choice = random.choice(deck.cards)
    hand.cards.append(choice)
    deck.cards.remove(choice)
    load_hand()
    updateLocations()

def pickup_discard(hand):
    choice = discard_pile.cards[-1]
    hand.cards.append(choice)
    discard_pile.cards.remove(choice)
    load_hand()
    updateLocations()

def discard(hand, active_card):
    hand.cards.remove(active_card)
    discard_pile.cards.append(active_card)
    load_hand()
    updateLocations()

def load_hand():
    for card in hand.cards:
        card_images[card.name] = pygame.image.load(f'gin/assets/cards/{card.name}')

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

    for cards in rank_groups.values():
        if len(cards) >= 3:
            all_melds.append(cards)

    for suit, cards in suit_groups.items():
        cards.sort()
        run = [cards[0][1]]
        for i in range(1, len(cards)):
            if cards[i][0] == cards[i - 1][0] + 1:
                run.append(cards[i][1])
            else:
                if len(run) >= 3:
                    all_melds.append(run[:])
                run = [cards[i][1]]
        if len(run) >= 3:
            all_melds.append(run[:])

    best_melds = []
    best_covered = set()

    from itertools import combinations

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
            if valid and len(used) > len(best_covered):
                best_melds = list(combo)
                best_covered = used

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
            deadwood += card_data[card.name]["rank"]

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

def computer_play():
    #find computer melds
    opp_hand.melds = update_melds(opp_hand)
    meld_cards = []
    for meld in opp_hand.melds:
        for card in meld:
            meld_cards.append(card)
    
    #pickup logic
    pickup_dis = False   
    for card in opp_hand.cards:
        if (abs(card_data[discard_pile.cards[-1].name]["rank"] - card_data[card.name]["rank"]) == 1 and 
            card_data[discard_pile.cards[-1].name]["suit"] == card_data[card.name]["suit"] and
            (get_meld_type_from_card(card, opp_hand.melds) == "run" or get_meld_type_from_card(card, opp_hand.melds) == "none")):
            pickup_discard(opp_hand)
            pickup_dis = True
            break
        elif (card_data[discard_pile.cards[-1].name]["rank"] == card_data[card.name]["rank"] and
            (get_meld_type_from_card(card, opp_hand.melds) == "set" or get_meld_type_from_card(card, opp_hand.melds) == "none")):
            pickup_discard(opp_hand)
            pickup_dis = True
            break

    if not pickup_dis:
        drawCard(deck, opp_hand)
        sort_cards_rank(opp_hand)

    #update melds after pickup
    opp_hand.melds = update_melds(opp_hand)
    meld_cards = []
    for meld in opp_hand.melds:
        for card in meld:
            meld_cards.append(card)

    #discard logic
    keep = []
    for card in opp_hand.cards:
        for other_card in opp_hand.cards:
            if (card_data[card.name]["rank"] == card_data[other_card.name]["rank"] and 
                card != other_card):
                keep.append(card)
            elif (card_data[card.name]["suit"] == card_data[other_card.name]["suit"] and 
                abs(card_data[card.name]["rank"] - card_data[other_card.name]["rank"]) == 1 and
                card != other_card):
                keep.append(card)
    
    pos_cards = [] #piece of shit cards
    for card in opp_hand.cards:
        if card not in keep:
            pos_cards.append(card)
    greatest_pos = 0
    pos = None
    for card in pos_cards:
        if card_data[card.name]["rank"] > greatest_pos:
            greatest_pos = card_data[card.name]["rank"]
            pos = card

    if pos:
        discard(opp_hand, pos)

    else:
        invaluables = []

        for card in opp_hand.cards:
            for dis in discard_pile.cards:

                if (card_data[card.name]["rank"] == card_data[dis.name]["rank"] and
                    card not in meld_cards):
                    invaluables.append(card)
                    break

                elif (card_data[card.name]["suit"] == card_data[dis.name]["suit"] and 
                    abs(card_data[card.name]["rank"] - card_data[dis.name]["rank"]) == 1 and
                    card not in meld_cards):
                    invaluables.append(card)
                    break

        trash = None

        if invaluables:
            greatest_num = 0
            for card in invaluables:
                if card_data[card.name]["rank"] > greatest_num:
                    greatest_num = card_data[card.name]["rank"]
                    trash = card
            discard(opp_hand, trash)

        else:
            cts = [] #contributes to set
            ctr = [] #contributes to run
            for card in opp_hand.cards:
                for other_card in opp_hand.cards:
                    if card != other_card:
                        if (card_data[card.name]["rank"] == card_data[other_card.name]["rank"]):
                            if (num_of_melds(other_card, opp_hand.melds) == 1 and 
                                get_meld_type_from_card(other_card, opp_hand.melds) == "run" and 
                                get_meld_type_from_card(card, opp_hand.melds) == "none"):
                                discard(opp_hand, card)
                                return
                            cts.append(card)
                        elif (card_data[card.name]["suit"] == card_data[other_card.name]["suit"] and
                            abs(card_data[card.name]["rank"] - card_data[other_card.name]["rank"]) == 1):
                            if (num_of_melds(other_card, opp_hand.melds) == 1 and 
                                get_meld_type_from_card(other_card, opp_hand.melds) == "set" and 
                                get_meld_type_from_card(card, opp_hand.melds) == "none"):
                                discard(opp_hand, card)
                                return
                            ctr.append(card)

            greatest_num = 0
            greatest_card = None
            both = []
            for card in opp_hand.cards:
                if card in cts and card in ctr:
                    both.append(card)
            for card in both:
                if card_data[card.name]["rank"] > greatest_num:
                    greatest_card = card
                    greatest_num = card_data[card.name]["rank"]

            if not both:
                for card in opp_hand.cards:
                    if card_data[card.name]["rank"] > greatest_num:
                        greatest_card = card
                        greatest_num = card_data[card.name]["rank"]
                discard(opp_hand, greatest_card)
                return

            random_number = random.randint(0, 1)
            for card in opp_hand.cards:
                if random_number == 0:
                    if (card_data[card.name]["rank"] == card_data[greatest_card.name]["rank"] and
                        card != greatest_card):
                        discard(opp_hand, card)
                        return
                else:
                    if (abs(card_data[card.name]["rank"] - card_data[greatest_card.name]["rank"]) == 1 and
                        card_data[card.name]["suit"] == card_data[greatest_card.name]["suit"] and 
                        card != greatest_card):
                        discard(opp_hand, card)
                        return

    #knocking/gin logic
    opp_hand.melds = update_melds(opp_hand)

    #deadwood = calculate_deadwood(opp_hand.melds, opp_hand.cards)

    #if deadwood == 0:
        #opp_hand.can_knock = True
    #elif deadwood <= 10:
        #opp_hand.can_knock = True

def show_start_screen():
    #moving background
    title_background = pygame.image.load(f'gin/assets/title_background.png').convert_alpha()
    tb_width = title_background.get_width()
    x_offset = 0.0
    background_clock = pygame.time.Clock()

    text_alpha = 255
    title_size = 140
    animating = False
    anim_frames = 20
    frame = 0

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  #start game on enter key
                    animating = True

        x_offset -= 0.5
        if x_offset <= -tb_width:
            x_offset = 0
        display_surface.blit(title_background, (int(x_offset), 0))
        display_surface.blit(title_background, (int(x_offset + tb_width), 0))

        if animating and frame < anim_frames:
            factor = frame / anim_frames
            exponential = 1 - (1-factor) ** 2
            title_size = 140 + 40 * exponential
            text_alpha = (255 * (1 - exponential))
            frame += 2
        elif animating and frame >= anim_frames: #continues to scroll the background after the title fades
            for _ in range(60):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                x_offset -= 0.5
                if x_offset <= -tb_width:
                    x_offset = 0

                display_surface.blit(title_background, (int(x_offset), 0))
                display_surface.blit(title_background, (int(x_offset + tb_width), 0))
                display_surface.blit(start_text, start_rect)

                pygame.display.flip()
                background_clock.tick(60)

            waiting = False

        title_font = pygame.font.Font('gin/assets/fonts/Mermaid1001.ttf', round(title_size))
        title_text = title_font.render("Gin Rummy", True, (255,222,133))
        title_text.set_alpha(text_alpha)
        start_text = small_font.render("Press ENTER to Start", True, (255,222,133))
        title_rect = title_text.get_rect(center=(displayWidth / 2, displayHeight * 5/12))
        start_rect = start_text.get_rect(center=(displayWidth // 2, displayHeight // 2))
        display_surface.blit(title_text, title_rect)
        display_surface.blit(start_text, start_rect)

        pygame.display.flip()
        background_clock.tick(60)

def update_menu_rects():
    global r_option_rect, mm_option_rect, c_option_rect, s_option_rect, qg_option_rect

    option_width = displayWidth / 10
    option_height = displayHeight / 15
    option_left = menu_x + menu_width / 2 - option_width / 2
    option_top = displayHeight / 11

    r_option_rect = pygame.Rect(option_left, option_top, option_width, option_height)
    mm_option_rect = pygame.Rect(option_left, option_top * 2, option_width, option_height)
    c_option_rect = pygame.Rect(option_left, option_top * 3, option_width, option_height)
    s_option_rect = pygame.Rect(option_left, option_top * 4, option_width, option_height)
    qg_option_rect = pygame.Rect(option_left, option_top * 5, option_width, option_height)

show_start_screen()
updateLocations()
sort_cards_rank(opp_hand)
load_hand()

while running:
    dt = clock.tick(120) / 1000 #fps
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        #game mouse detection
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:

                if menu_rect.collidepoint(event.pos):
                    menu_overlay = True

                if main_menu_overlay_rect.collidepoint(event.pos): #close the menu if it's open and you click off
                    menu_overlay = False
                
                if menu_overlay: #menu options
                    update_menu_rects()
                    if mm_option_rect.collidepoint(event.pos):
                        restart_from_main_menu = True
                    if qg_option_rect.collidepoint(event.pos):
                        running = False

                for card in reversed(hand.cards):
                    if card == hand.cards[-1]:      #if card is on the right, it's rect is larger
                        card_rect = pygame.Rect(card.loc[0], card.loc[1], 73, 98)
                    else:                           #else we need to modify the rect to match the size
                        card_rect = pygame.Rect(card.loc[0], card.loc[1], ((display_surface.get_width() / 3) / (len(hand.cards) - 1)) * 0.8, 98)

                    if card_rect.collidepoint(event.pos): #if mousedown on a card rect
                        clicked = True
                        active_card = card
                        active_card.dragging = True
                        original_loc = active_card.loc
                        original_index = hand.cards.index(active_card)
                        card_x = event.pos[0] - active_card.loc[0]
                        card_y = event.pos[1] - active_card.loc[1]
                        break
                    elif draw_rect.collidepoint(event.pos):
                        if turn == 1:
                            drawCard(deck, hand)
                            horizontal_shift = (((display_surface.get_width() / 3) / len(hand.cards)) * 0.8)
                            hand.melds = update_melds(hand)
                            if can_knock(hand.melds, hand.cards):
                                hand.can_knock = True
                            turn *= -1
                        break
                    elif discard_rect.collidepoint(event.pos):
                        if turn == 1:
                            pickup_discard(hand)
                            horizontal_shift = (((display_surface.get_width() / 3) / len(hand.cards)) * 0.8)
                            hand.melds = update_melds(hand)
                            if can_knock(hand.melds, hand.cards):
                                hand.can_knock = True
                            if discard_pile.cards:
                                discard_top = pygame.image.load(f'gin/assets/cards/{discard_pile.cards[-1].name}')
                            turn *= -1
                            break
                    elif sort_rect_rank.collidepoint(event.pos):
                        sort_cards_rank(hand)
                    elif sort_rect_suit.collidepoint(event.pos):
                        sort_cards_suit(hand)
                    elif player_knock_rect.collidepoint(event.pos):
                        if turn == -1:
                            round_overlay = True
                            player_knock = True

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

                if discard_rect.collidepoint(event.pos) and turn == -1:
                    discard(hand, active_card)
                    horizontal_shift = (((display_surface.get_width() / 3) / len(hand.cards)) * 0.8)
                    discard_top = pygame.image.load(f'gin/assets/cards/{discard_pile.cards[-1].name}')
                    turn *= -1
                    player_turn *= -1
                updateLocations()

                for card in hand.cards:
                    card.hovered_x = False

                active_card = None
                clicked = False

    #hover_y logic
    mouse_x, mouse_y = pygame.mouse.get_pos()
    hover_candidate_y = None

    for card in reversed(hand.cards):
        if card.dragging:
            continue
        width = 73 if card == hand.cards[-1] else (display_surface.get_width() / 3) / max(len(hand.cards) - 1, 1) * 0.8
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

    display_surface.blit(background, (0, 0)) #background

    #menu overlay
    if menu_overlay: #opening the menu

        hamburger_tx = -1.5 * hamburger_width
        menu_tx = 0
        hamburger_x = max(hamburger_x - (menu_speed * dt), hamburger_tx)
        menu_x = min(menu_x + (menu_speed * dt), menu_tx)
        display_surface.blit(side_overlay, (menu_x,0))

        option_width = displayWidth/10
        option_height = displayHeight/15
        option_left = menu_x + menu_width/2 - option_width/2
        option_top = displayHeight/11
        r_option_rect = pygame.Rect(option_left, option_top, option_width, option_height) #retry option
        r_option_text = medium_font.render("Retry", True, WHITE)
        mm_option_rect = pygame.Rect(option_left, option_top*2, option_width, option_height) #main menu option
        mm_option_text = medium_font.render("Main Menu", True, WHITE)
        c_option_rect = pygame.Rect(option_left, option_top*3, option_width, option_height) #customize option
        c_option_text = medium_font.render("Customize", True, WHITE)
        s_option_rect = pygame.Rect(option_left, option_top*4, option_width, option_height) #settings option
        s_option_text = medium_font.render("Settings", True, WHITE)
        qg_option_rect = pygame.Rect(option_left, option_top*5, option_width, option_height) #quit game option
        qg_option_text = medium_font.render("Quit Game", True, WHITE)

        display_surface.blit(r_option_text, r_option_text.get_rect(center=r_option_rect.center)) #retry option
        display_surface.blit(mm_option_text, mm_option_text.get_rect(center=mm_option_rect.center)) #main menu option
        display_surface.blit(c_option_text, c_option_text.get_rect(center=c_option_rect.center)) #customize option
        display_surface.blit(s_option_text, s_option_text.get_rect(center=s_option_rect.center)) #settings option
        display_surface.blit(qg_option_text, qg_option_text.get_rect(center=qg_option_rect.center)) #quit game option


    else: #closing the menu

        display_surface.blit(side_overlay, (menu_x, 0))
        hamburger_tx = 30
        menu_tx = -1.5 * menu_width
        hamburger_x = min(hamburger_x + (menu_speed * dt), hamburger_tx)
        menu_x = max(menu_x - (menu_speed * dt), menu_tx)

    #menu icon
    pygame.draw.rect(display_surface, "white", pygame.Rect(hamburger_x,30,hamburger_width,8))
    pygame.draw.rect(display_surface, "white", pygame.Rect(hamburger_x,45,hamburger_width,8))
    pygame.draw.rect(display_surface, "white", pygame.Rect(hamburger_x,60,hamburger_width,8))

    #player knock button
    if hand.can_knock:
        pygame.draw.rect(display_surface, (200, 200, 200), player_knock_rect, border_radius=8)
        pygame.draw.rect(display_surface, BLACK, player_knock_rect, 2, border_radius=8)
        display_surface.blit(player_knock_text, knock_player_rect)

    #opponent knock button
    if opp_hand.can_knock:
        pygame.draw.rect(display_surface, (200, 200, 200), opp_knock_rect, border_radius=8)
        pygame.draw.rect(display_surface, BLACK, opp_knock_rect, 2, border_radius=8)
        display_surface.blit(opp_knock_text, knock_opp_rect)

    #sort rect
    pygame.draw.rect(display_surface, (200, 200, 200), sort_rect_rank, border_radius=8)
    pygame.draw.rect(display_surface, BLACK, sort_rect_rank, 2, border_radius=8)
    pygame.draw.rect(display_surface, (200, 200, 200), sort_rect_suit, border_radius=8)
    pygame.draw.rect(display_surface, BLACK, sort_rect_suit, 2, border_radius=8)
    display_surface.blit(sort_rank_text, sort_rank_rect)
    display_surface.blit(sort_suit_text, sort_suit_rect)

    #outline when discard pile is empty
    pygame.draw.rect(display_surface, "white", pygame.Rect(display_surface.get_width() * 5/9 - blue_back.get_width() / 2, display_surface.get_height() / 2 - blue_back.get_height() / 2, 73, 98), 4, border_radius=10)
    display_surface.blit(blue_back, (display_surface.get_width() * 4/9 - blue_back.get_width() / 2, display_surface.get_height() / 2 - blue_back.get_height() / 2))
    if discard_pile.cards:
        display_surface.blit(discard_top, (display_surface.get_width() * 5/9 - blue_back.get_width() / 2, display_surface.get_height() / 2 - blue_back.get_height() / 2))

    #drawing the opponents hand
    for card in opp_hand.cards:
        display_surface.blit(blue_back, card.loc)

    #drawing the hand while you're holding a card
    if active_card:
        active_card_x = active_card.loc[0]
        for card in hand.cards:
            if card.loc[0] < active_card_x: #draw all the card before the active card first
                display_surface.blit(card_images[card.name], (card.loc))
        display_surface.blit(card_images[active_card.name], (active_card.loc)) #draw the active card
        for card in hand.cards:
            if card.loc[0] > active_card_x: #draw all the cards after the active card last
                display_surface.blit(card_images[card.name], (card.loc))
    else:
        for card in hand.cards:
            display_surface.blit(card_images[card.name], (card.loc))
    
    #round overlay
    if round_overlay:
        overlay = pygame.Surface(display_surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        display_surface.blit(overlay, (0, 0))
        continue_text = small_font.render("Press ENTER to continue", True, WHITE)
        hand.melds = update_melds(hand)
        opp_hand.melds = update_melds(opp_hand)
        
    
        if player_knock: #player knock logic
            opp_meld_cards = []
            opp_deadwood = []
            opp_deadwood_score = 0
            player_deadwood_score = calculate_deadwood(hand.melds, hand.cards)
            laid_off = []
            for meld in opp_hand.melds:
                for card in meld:
                    opp_meld_cards.append(card)
            for card in opp_hand.cards:
                if card not in opp_meld_cards:
                    opp_deadwood.append(card)
            
            for meld in hand.melds:
                for card in opp_deadwood:
                    if can_contribute(card, meld):
                        if card not in laid_off:
                            laid_off.append(card)

            for card in opp_deadwood:
                if card not in laid_off:
                    if card_data[card.name]["rank"] > 10:
                        opp_deadwood_score += 10
                    else:
                        opp_deadwood_score += card_data[card.name]["rank"]
            
            player_knock = False

        else:

            pass #opponent knock logic [WIP]

        if opp_deadwood_score > player_deadwood_score:
            hand.score += (opp_deadwood_score - player_deadwood_score)
        

        player_score_text = small_font.render(f"Player: {player_deadwood_score}", True, WHITE)
        opp_score_text = small_font.render(f"Opponent: {opp_deadwood_score}", True, WHITE)


        display_surface.blit(continue_text, continue_text.get_rect(center=(displayWidth // 2, displayHeight * 2/3)))
        display_surface.blit(player_score_text, player_score_text.get_rect(center=(displayWidth // 2, displayHeight * 1/3)))
        display_surface.blit(opp_score_text, opp_score_text.get_rect(center=(displayWidth // 2, (displayHeight * 1/3) + 25)))
        round_overlay = False
    
    #advance the turn
    if (player_turn == -1):
        computer_play()
        sort_cards_rank(opp_hand)
        discard_top = pygame.image.load(f'gin/assets/cards/{discard_pile.cards[-1].name}')
        player_turn *= -1

    #restart from title screen
    if restart_from_main_menu:
        show_start_screen()
        menu_overlay = False
        deck = Deck()
        hand = Hand(deck)
        discard_pile = DiscardPile(deck)
        opp_hand = Hand(deck)
        updateLocations()
        sort_cards_rank(opp_hand)
        load_hand()
        restart_from_main_menu = False

    pygame.display.flip()

pygame.quit()

