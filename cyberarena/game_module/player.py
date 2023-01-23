from typing import Optional

from loguru import logger

from cyberarena.game_module.card import AbstractCard
from cyberarena.game_module.deck import Deck
from cyberarena.game_module.hand import Hand


class Player:
    """Player Class."""

    id = 0

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
        self.__hand.get_random_card(self.id)
        self.id += 1

    def use_card(self, card: AbstractCard) -> Optional[AbstractCard]:
        """
        Use a card.

        :param card: Card to use.
        :return: the card used or a card with name "None".
        """
        res: AbstractCard = self.__hand.use_card(card, self.mana)
        if res.cost != 0:
            self.mana -= res.cost
            logger.debug("Card used")
            return res
        logger.debug("Card not used")
        return None

    def use_card_debug(self, index: int) -> Optional[AbstractCard]:
        """
        Use a card debug mode.

        :param index: index of the card to get.
        :return: the card used or a card with name "None".
        """
        res: AbstractCard = self.__hand.use_card_debug(index, self.mana)
        if res.cost != 0:
            self.mana -= res.cost
            logger.debug("Card used")
            return res
        logger.debug("Card not used")
        return None

    def get_card_from_hand_id(self, idcard: int) -> Optional[AbstractCard]:
        """
        Get a card from the hand.

        :param idcard: ID of the card.
        :return: The card.
        """
        return self.__hand.get_card_id(idcard)

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

    def cheat_add_card_to_hand(self, card: AbstractCard) -> None:
        """
        Add a card to the hand.

        :param card: Card to add.
        """
        self.__hand.cheat_add_card(card, self.id)
        self.id += 1
