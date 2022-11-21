from random import random
from typing import List

from cyberarena.src import Card


class Deck:
    def __init__(self):
        self.card: List[Card] = []
        self.deckSize = 20
        self.initDeck()

    def initDeck(self) -> None:
        for x in range(0, self.deckSize):
            self.card.append(
                Card.Card("Cyber-Heisenberg", 1, 1, 1, 1, "Walter White en Personne")
            )

    def getDeckSize(self) -> int:
        return len(self.card)

    def getRandomCard(self) -> Card:
        if len(self.card) < 0:
            return None
        rand = random.randint(0, len(self.card) - 1)
        card = self.card[rand]
        cardSave = card
        self.card.remove(card)
        return cardSave

    def getCard(self, card: Card) -> Card:
        for x in self.card:
            if x == card:
                xsave = x
                self.card.remove(x)
                return xsave
        return None
