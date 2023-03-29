from typing import Optional

from loguru import logger

from .card import AbstractCard
from .deck import Deck
from .hand import Hand
from .settings import settings


class Player:
    """Player Class."""

    id = -1

    def __init__(self, name: str = "", test: bool = False) -> None:
        """
        Constructor.

        :param name: Name of the player.
        :param test: True if the game is in test mode, False otherwise.
        """
        self.name = name
        self.__hand = Hand(test)
        self.life = 20
        self.mana = settings.mana_initial
        self.mana_max_turn = settings.mana_initial
        self.mana_max = settings.mana_max
        self.idcardcurr = 0

    def get_mana(self) -> int:
        """
        Get the mana of the player.

        :return: The mana of the player.
        """
        return self.mana

    def draw_card(self) -> Optional[AbstractCard]:
        """
        Draw a card.

        :return: The card drawn.
        """
        card = self.__hand.get_random_card(self.idcardcurr)
        self.idcardcurr += 1
        return card

    def use_card(self, card: AbstractCard) -> Optional[AbstractCard]:
        """
        Use a card.

        :param card: Card to use.
        :return: the card used or a card with name "None".
        """
        res: AbstractCard = self.__hand.use_card(card, self.mana)
        if res.cost != 0:
            self.mana -= res.cost
            return res
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
            return res
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
        return self.__hand.get_deck()

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
        self.__hand.cheat_add_card(card, self.idcardcurr)
        self.idcardcurr += 1

    def next_turn(self) -> None:
        """Next turn."""
        if self.mana_max_turn >= self.mana_max:
            self.mana = self.mana_max_turn
            return
        self.mana_max_turn += settings.mana_increase_turn
        self.mana = self.mana_max_turn

    def get_hand(self) -> Hand:
        """
        Get the hand of the player.

        :return: The hand of the player.
        """
        return self.__hand

    def display_hand(self) -> None:
        """Display the hand."""
        for i in range(0, len(self.__hand)):
            logger.error(self.__hand.get_hand()[i].to_dict())
