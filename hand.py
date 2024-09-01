import random

class Hand:
    cards = []
    def __init__(self):
        self.cards = []

    def __init__(self, deck):
        self.cards = []

        for x in range(10):
            choice = random.choice(deck.cards)
            self.cards.append(choice)
            deck.cards.remove(choice)

        i = 0
        for card in self.cards:
            card.loc = (i * 73, 0)
            i = i + 1

            
