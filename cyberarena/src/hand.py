from typing import List, Optional

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

    def get_random_card(self) -> Optional[Card]:
        """
        Get a random card from the hand.

        :return: A random card from the deck.
        """
        card = self.__Deck.get_random_card()
        if card:
            self.__hand.append(card)
        return self.__Deck.get_random_card()

    def use_card(self, card: Card, mana: int) -> Card:
        """
        Use a card.

        :param card: Card to use.
        :param mana: mana of the player.
        :return: True if the card is used, False otherwise.
        """
        if card.cost <= mana:
            self.__hand.remove(card)
            return card
        return Card("None", 0, 0, 0)

    def use_card_debug(self, index: int, mana: int) -> Card:
        """
        Use a card.

        :param index: index of the card tu get.
        :param mana: mana of the player.
        :return: True if the card is used, False otherwise.
        """
        card = self.__hand[index]
        if self.__hand[index].cost <= mana:
            self.__hand.remove(self.__hand[index])
            return card
        return Card("None", 0, 0, 0)

    def get_hand(self) -> List[Card]:
        """
        Get the hand.

        :return: The hand.
        """
        return self.__hand
