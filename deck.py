import os
from card import Card

class Deck:
    def __init__(self) -> None:
        self.cards = []
        for filename in os.listdir("C:/Users/polak/Desktop/GinProject/assets/cards"):
            card = Card(filename, None)
            self.cards.append(card)