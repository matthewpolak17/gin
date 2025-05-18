import os
from card import Card

class Deck:
    def __init__(self) -> None:
        self.cards = []
        for filename in os.listdir("./gin/assets/cards"):
            card = Card(filename, None)
            self.cards.append(card)