from typing import List

from cyberarena.src import Card, Deck


class Hand :
    def __init__(self) :
        self.card:List[Card] = []
    def getFirstHand(self) -> None:
        for x in range(0,10) :
            self.card.append(Deck.getRandomCard())
    def getNextCard(self) -> None:
        card : Card = Deck.getRandomCard()
        if card != None:
            self.card.append(Deck.getRandomCard())
    def useCard(self,card : Card) -> Card :
        for x in self.card:
            if x == card:
                xsave = x
                self.card.remove(x)
                return xsave

