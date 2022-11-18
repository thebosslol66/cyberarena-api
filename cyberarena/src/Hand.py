class Hand :
    def __init__(self) :
        self.card = []

    def getFirstHand(self):
        for x in range(0,10) :
            self.card.append(Deck.getRandomCard())

    def getNextCard(self):
        self.card.append(Deck.getRandomCard())

    def getCardFromHand(self,card):

