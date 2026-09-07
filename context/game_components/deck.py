from context.game_components.card import Card
import os

class Deck:
    def __init__(self) -> None:
        self.cards = []
        #for filename in os.listdir("./assets/cards"):
        for filename in os.listdir("./assets/images/custom_cards/new"):
            card = Card(filename, None)
            self.cards.append(card)