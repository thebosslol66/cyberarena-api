from cyberarena.src.card import Card
from cyberarena.src.deck import Deck
from cyberarena.src.hand import Hand


class Player:
    """Player Class."""

    def __init__(self, name: str) -> None:
        """
        Constructor.

        :param name: Name of the player.
        """
        self.name = name
        self.__deck = Deck()
        self.__hand = Hand(self.__deck)
        self.life = 20
        self.mana = 0
        self.mana_max = 10

    def get_mana(self) -> int:
        """
        Get the mana of the player.

        :return: The mana of the player.
        """
        return self.mana

    def draw_card(self) -> None:
        """Draw a card."""
        self.__hand.get_random_card()

    def use_card(self, card: Card) -> Card:
        """
        Use a card.

        :param card: Card to use.
        :return: the card used or a card with name "None".
        """
        res: Card = self.__hand.use_card(card, self.mana)
        if res.cost != 0:
            self.mana -= res.cost
            print("Card used")
            return res
        print("Card not used")
        return Card("None", 0, 0, 0, 0)

    def use_card_debug(self, index: int) -> Card:
        """
        Use a card.

        :param index: index of the card to get.
        :return: the card used or a card with name "None".
        """
        res: Card = self.__hand.use_card_debug(index, self.mana)
        if res.cost != 0:
            self.mana -= res.cost
            print("Card used")
            return res
        print("Card not used")
        return Card("None", 0, 0, 0, 0)

    def increase_mana(self, value: int) -> int:
        """
        Increase the mana of the player.

        :param value: Value to increase.
        :return: The new mana value.
        """
        self.mana += value
        if self.mana > self.mana_max:
            self.mana = self.mana_max
        return self.mana

    def debug_get_deck(self) -> Deck:
        """
        Get the deck of the player.

        :return: The deck of the player.
        """
        return self.__deck

    def debug_get_hand(self) -> Hand:
        """
        Get the hand of the player.

        :return: The hand of the player.
        """
        return self.__hand
