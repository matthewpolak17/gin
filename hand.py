import random

class Hand:
    cards = []
    can_knock = False
    melds = []
    score = 0
    def __init__(self):
        self.cards = []
        self.melds = []
        self.can_knock = False
        self.score = 0

    def __init__(self, deck):
        self.cards = []
        self.melds = []
        self.can_knock = False
        self.score = 0
        
        for x in range(10):
            choice = random.choice(deck.cards)
            self.cards.append(choice)
            deck.cards.remove(choice)

        i = 0
        for card in self.cards:
            card.loc = (i * 73, 0)
            i = i + 1

            
