import pygame
import random
import csv
from deck import Deck
from hand import Hand
from discard_pile import DiscardPile

# setup
pygame.init()
displayHeight = 900
displayWidth = 500
display_surface = pygame.display.set_mode((displayHeight, displayWidth), pygame.RESIZABLE)
display_surface.fill((255, 255, 255))
clock = pygame.time.Clock()
running = True
dropped = False
dt = 0
deck = Deck()
hand = Hand(deck)
discard_pile = DiscardPile(deck)
discard_top = None
opp_hand = Hand(deck)
original_loc = (0, 0)
clicked = False
dropped_card = None
active_card = None
card_images = {}
turn = 1
player_turn = 1
card_data = {}

with open('./assets/card_values.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        card_data[row['name']] = {'suit': row['suit'], 'rank': int(row['rank'])}

#functions
def updateLocations():
    i = 0
    win_width = display_surface.get_width() / 3
    vert_middle = display_surface.get_height() / 2
    for card in hand.cards:
        card.loc = (win_width + i - 36, 1.5*vert_middle)
        i = i + win_width / (len(hand.cards) - 1)
    i = 0
    for card in opp_hand.cards:
        card.loc = (win_width + i - 36, vert_middle/2 - 98)
        i = i + win_width / (len(opp_hand.cards) - 1)

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
        card_images[card.name] = pygame.image.load(f'assets/cards/{card.name}')

def computer_play():
    pickup_discard(opp_hand)
    discard(opp_hand, opp_hand.cards[5])

def sort_cards(hand):
    sorted_hand = []
    while hand.cards:
        card = hand.cards.pop(0)
        num = card_data[card.name]['rank']
        same_rank_cards = [card]
        for other_card in hand.cards[:]:
            if card_data[other_card.name]['rank'] == num:
                same_rank_cards.append(other_card)
                hand.cards.remove(other_card)
        sorted_hand.extend(same_rank_cards)
    hand.cards = sorted_hand
    updateLocations()


background = pygame.image.load(r'./assets/background.png')
blue_back = pygame.image.load(r'./assets/blueback.png')
blue_back = pygame.transform.scale(blue_back, (73, 98))
draw_rect = pygame.Rect(display_surface.get_width() * 4/9 - blue_back.get_width() / 2, display_surface.get_height() / 2 - blue_back.get_height() / 2, 73, 98)
discard_rect = pygame.Rect(display_surface.get_width() * 5/9 - blue_back.get_width() / 2, display_surface.get_height() / 2 - blue_back.get_height() / 2, 73, 98)
discard_top = pygame.image.load(f'assets/cards/{discard_pile.cards[-1].name}')

updateLocations()
load_hand()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #mouse detection
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for card in hand.cards:
                if card == hand.cards[-1]:
                    card_rect = pygame.Rect(card.loc[0], card.loc[1], 73, 98)
                else:
                    card_rect = pygame.Rect(card.loc[0], card.loc[1], ((display_surface.get_width() / 3) / (len(hand.cards) - 1)), 98)
                if card_rect.collidepoint(event.pos):
                    clicked = True
                    active_card = card
                    original_loc = active_card.loc
                    card_x = event.pos[0] - active_card.loc[0]
                    card_y = event.pos[1] - active_card.loc[1]
                elif draw_rect.collidepoint(event.pos):
                    if turn == 1:
                        drawCard(deck, hand)
                        turn *= -1
                    break
                elif discard_rect.collidepoint(event.pos):
                    if turn == 1:
                        pickup_discard(hand)
                        if discard_pile.cards:
                            discard_top = pygame.image.load(f'assets/cards/{discard_pile.cards[-1].name}')
                        turn *= -1

        elif event.type == pygame.MOUSEMOTION and clicked == True:
            active_card.loc = (event.pos[0] - card_x, event.pos[1] - card_y)
        elif event.type == pygame.MOUSEMOTION:
            #print(event.pos)
            pass
        elif event.type == pygame.MOUSEBUTTONUP:
            
            for card in hand.cards:
                card_width = 73 if card == hand.cards[-1] else (display_surface.get_width() / 3) / (len(hand.cards) - 1)
                card_rect = pygame.Rect(card.loc[0], card.loc[1], card_width, 98) #draw a rectangle for that card
                if card_rect.collidepoint(event.pos) and card != active_card and active_card != None: #if mouse is over the card and it's not the card you're holding
                    dropped_card = card 
                    break
                elif discard_rect.collidepoint(event.pos) and turn == -1 and active_card != None:
                    discard(hand, active_card)
                    dropped_card = None
                    discard_top = pygame.image.load(f'assets/cards/{discard_pile.cards[-1].name}')
                    turn *= -1
                    player_turn *= -1
                    sort_cards(hand)
                    break  
                else:
                    dropped_card = None

            
            if dropped_card == None and clicked == True:
                active_card.loc = original_loc #put the card back where it was
            elif dropped_card != None:
                active_index = hand.cards.index(active_card)
                drop_index = hand.cards.index(dropped_card)
                if active_index < drop_index: #moving card to the right
                    placeholder = active_card
                    for i in range(active_index, drop_index, 1):
                        hand.cards[i] = hand.cards[i+1]
                    hand.cards[drop_index] = placeholder
                elif active_index > drop_index: #moving card to the left
                    placeholder = active_card
                    for i in range(active_index, drop_index, -1):
                        hand.cards[i] = hand.cards[i-1]
                    hand.cards[drop_index] = placeholder
                updateLocations()

            active_card = None
            clicked = False
        elif event.type == pygame.WINDOWRESIZED:
            updateLocations()
            discard_rect = pygame.Rect(display_surface.get_width() * 5/9 - blue_back.get_width() / 2, display_surface.get_height() / 2 - blue_back.get_height() / 2, 73, 98)
            draw_rect = pygame.Rect(display_surface.get_width() * 4/9 - blue_back.get_width() / 2, display_surface.get_height() / 2 - blue_back.get_height() / 2, 73, 98)
            background = pygame.transform.scale(background, display_surface.get_size())
    """
    #card hover
    mouse_pos = pygame.mouse.get_pos()
    for card in hand.cards:
        card_width = 73 if card == hand.cards[-1] else (display_surface.get_width() / 3) / (len(hand.cards) - 1)
        hover_height_extension = card.hover_offset if card.is_hovered else 0
        card_rect = pygame.Rect(card.loc[0], card.loc[1], card_width, 98 + hover_height_extension)

        if card_rect.collidepoint(mouse_pos) and not card.is_hovered:
            card.loc = (card.loc[0], card.loc[1] - card.hover_offset)
            card.is_hovered = True

        elif not card_rect.collidepoint(mouse_pos) and card.is_hovered:
            card.loc = (card.loc[0], card.loc[1] + card.hover_offset)
            card.is_hovered = False
    """
    display_surface.blit(background, (0, 0)) #background
    pygame.draw.rect(display_surface, "white", pygame.Rect(30,30,30,5)) #menu icon
    pygame.draw.rect(display_surface, "white", pygame.Rect(30,40,30,5)) #menu icon
    pygame.draw.rect(display_surface, "white", pygame.Rect(30,50,30,5)) #menu icon

    pygame.draw.rect(display_surface, "white", pygame.Rect(display_surface.get_width() * 5/9 - blue_back.get_width() / 2, display_surface.get_height() / 2 - blue_back.get_height() / 2, 73, 98), 4, border_radius=10)
    display_surface.blit(blue_back, (display_surface.get_width() * 4/9 - blue_back.get_width() / 2, display_surface.get_height() / 2 - blue_back.get_height() / 2))
    if discard_pile.cards:
        display_surface.blit(discard_top, (display_surface.get_width() * 5/9 - blue_back.get_width() / 2, display_surface.get_height() / 2 - blue_back.get_height() / 2))
    """
    for card in opp_hand.cards: #draws opp_hand
        display_surface.blit(blue_back, (card.loc))
    """
    for card in opp_hand.cards:
        display_surface.blit(pygame.image.load(f'assets/cards/{card.name}'), card.loc)

    if active_card:
        active_card_x = active_card.loc[0]
        for card in hand.cards:
            if card.loc[0] < active_card_x:
                display_surface.blit(card_images[card.name], (card.loc))
        display_surface.blit(card_images[active_card.name], (active_card.loc))
        for card in hand.cards:
            if card.loc[0] > active_card_x:
                display_surface.blit(card_images[card.name], (card.loc))
    else:
        for card in hand.cards:
            display_surface.blit(card_images[card.name], (card.loc))
    
    if (player_turn == -1):
        computer_play()
        sort_cards(opp_hand)
        discard_top = pygame.image.load(f'assets/cards/{discard_pile.cards[-1].name}')
        player_turn *= -1

    pygame.display.flip()
    dt = clock.tick(120) / 1000 #fps

pygame.quit()

