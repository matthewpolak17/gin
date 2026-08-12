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

    # def __init__(self, deck, test):
    #     if test:
    #         self.cards = []
    #         self.cards.extend(deck.cards)
    #         deck.cards.clear()
    #         deck.cards.append(self.cards[-1])

            
