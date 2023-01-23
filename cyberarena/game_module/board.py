from typing import List, Optional

from loguru import logger

from cyberarena.game_module.card import AbstractCard, PlayableCharacterCard
from cyberarena.game_module.settings import settings


class Board:
    """Board Class."""

    def __init__(self) -> None:
        """Constructor."""
        self.__side1: List[AbstractCard] = []
        self.__side2: List[AbstractCard] = []
        self.__boardSize = settings.board_size

    def deploy_card(self, card: AbstractCard, side: int) -> None:
        """
        Deploy a card.

        :param card: Card to deploy.
        :param side: Side of the board the card is being deployed in.
        """
        if side == 1:
            if len(self.__side1) < self.__boardSize:
                self.__side1.append(card)
            else:
                logger.debug("Board is full")
        else:
            if len(self.__side2) < self.__boardSize:
                self.__side2.append(card)
            else:
                logger.debug("Board is full")

    def show_board(self) -> None:
        """Show the board."""
        logger.debug("Side 1:")
        for card in self.__side1:
            logger.debug(card)
        logger.debug("Side 2:")
        for card in self.__side2:
            logger.debug(card)

    def attack_card(
        self,
        cardatt: AbstractCard,
        cardrecv: AbstractCard,
        side: int,
    ) -> None:
        """
        Attack a card.

        :param cardatt: Card attacking.
        :param cardrecv: Card receiving the attack.
        :param side: Side of the board of the card recving damage.
        """
        if isinstance(cardatt, PlayableCharacterCard) and isinstance(
            cardrecv,
            PlayableCharacterCard,
        ):
            cardatt.attack_card(cardrecv)
            if not cardrecv.is_alive():
                if side == 1:
                    self.__side1.remove(cardrecv)
                else:
                    self.__side2.remove(cardrecv)

    def get_board_size(self) -> int:
        """
        Get the size of the board.

        :return: The size of the board.
        """
        return len(self.__side1) + len(self.__side2)

    def get_max_board_size(self) -> int:
        """
        Get the max size of the board.

        :return: The max size of the board.
        """
        return self.__boardSize

    def get_card_debug(self, player: int, index: int) -> Optional[AbstractCard]:
        """
        Get a card debug mode.

        :param player: Player to get the card from.
        :param index: Index of the card to get.
        :return: The card.
        """
        if player == 1:
            if index > len(self.__side1):
                return None
            return self.__side1[index]
        if index > len(self.__side2):
            return None
        return self.__side2[index]

    def get_card_id(self, player: int, id: int) -> Optional[AbstractCard]:
        """
        Get a card by id.

        :param player: Player to get the card from.
        :param id: id of the card to get.
        :return: The card.
        """
        if player == 1:
            for card in self.__side1:
                if card.id == id:
                    return card
        else:
            for card in self.__side2:
                if card.id == id:
                    return card
        return None
