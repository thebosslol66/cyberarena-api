import logging
from typing import List, Optional

from .card import AbstractCard, PlayableCharacterCard
from .deck import Deck

logger = logging.getLogger("cyberarena.game_module")


class Hand:
    """Hand Class."""

    def __init__(self, deck: Deck) -> None:
        """
        Constructor.

        :param deck: Deck assigned to the Hand.
        """
        self.__hand: List[AbstractCard] = []
        self.__Deck = deck

    def __len__(self) -> int:
        """
        Get the hand size.

        :return: The hand size.
        """
        return len(self.__hand)

    def get_random_card(self, idcard: int) -> Optional[AbstractCard]:
        """
        Get a random card from the deck.

        :param idcard: ID of the card.
        :return: A random card from the deck.
        """
        card = self.__Deck.get_random_card()
        if card:
            card.id = idcard
            self.__hand.append(card)
        else:
            logger.debug("Deck is empty")
            return None
        return card

    def use_card(self, card: AbstractCard, mana: int) -> AbstractCard:
        """
        Use a card.

        :param card: Card to use.
        :param mana: mana of the player.
        :return: True if the card is used, False otherwise.
        """
        if card.cost <= mana:
            self.__hand.remove(card)
            return card
        return PlayableCharacterCard("None", 0, 0, 0, 0)

    def use_card_debug(self, index: int, mana: int) -> AbstractCard:
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
        return PlayableCharacterCard("None", 0, 0, 0, 0)

    def get_card_id(self, idcard: int) -> Optional[AbstractCard]:
        """
        Get a card by its ID.

        :param idcard: ID of the card.
        :return: The card.
        """
        for card in self.__hand:
            if card.id == idcard:
                return card
        return None

    def cheat_add_card(self, card: AbstractCard, idcard: int) -> None:
        """
        Add a card to the hand.

        :param card: Card to add.
        :param idcard: ID of the card.
        """
        card.id = idcard
        self.__hand.append(card)
