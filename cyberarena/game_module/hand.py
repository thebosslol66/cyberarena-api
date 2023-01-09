from typing import List, Optional

from cyberarena.game_module.card import PlayableCard
from cyberarena.game_module.deck import Deck


class Hand:
    """Hand Class."""

    def __init__(self, deck: Deck) -> None:
        """
        Constructor.

        :param deck: Deck assigned to the Hand.
        """
        self.__hand: List[PlayableCard] = []
        self.__Deck = deck

    def get_hand_size(self) -> int:
        """
        Get the hand size.

        :return: The hand size.
        """
        return len(self.__hand)

    def get_random_card(self) -> Optional[PlayableCard]:
        """
        Get a random card from the hand.

        :return: A random card from the deck.
        """
        card = self.__Deck.get_random_card()
        if card:
            self.__hand.append(card)
        return self.__Deck.get_random_card()

    def use_card(self, card: PlayableCard) -> None:
        """
        Use a card.

        :param card: Card to use.
        """
        self.__hand.remove(card)

    def use_card_debug(self, index: int) -> None:
        """
        Use a card.

        :param index: index of the card tu get.
        """
        self.__hand.remove(self.__hand[index])
