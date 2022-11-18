class Hand :
    def __init__(self) :
        self.card = []

    def getFirstHand(self) -> None:
        for x in range(0,10) :
            self.card.append(Deck.getRandomCard())


    def getNextCard(self) -> Card:
        self.card.append(Deck.getRandomCard())

    def getCardFromHand(self,card) -> Card:
        self.card.remove(card)
        return card
