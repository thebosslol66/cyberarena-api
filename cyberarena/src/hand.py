from typing import List

from cyberarena.src.card import Card
from cyberarena.src.deck import Deck


class Hand:
    """Hand Class."""

    def __init__(self, deck: Deck) -> None:
        """
        Constructor.

        :param deck: Deck assigned to the Hand.
        """
        self.__hand: List[Card] = []
        self.__Deck = deck

    def get_hand_size(self) -> int:
        """
        Get the hand size.

        :return: The hand size.
        """
        return len(self.__hand)

    def get_random_card(self) -> None:
        """Get a random card from the hand."""
        card = self.__Deck.get_random_card()
        if card is not None:
            self.__hand.append(card)

    def use_card(self, card: Card) -> None:
        """
        Use a card.

        :param card: Card to use.
        """
        self.__hand.remove(card)

    def use_card_debug(self, i: int) -> None:
        """
        Use a card.

        :param i: indice de la card to use.
        """
        self.__hand.remove(self.__hand[i])
