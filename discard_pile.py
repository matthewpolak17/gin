import random

class DiscardPile:
    cards = []
    def __init__(self):
        self.cards = []

    def __init__(self, deck):
        self.cards = []
        choice = random.choice(deck.cards)
        self.cards.append(choice)
        deck.cards.remove(choice)

            
