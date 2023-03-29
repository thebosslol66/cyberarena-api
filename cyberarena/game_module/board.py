import logging
from typing import Dict, List, Optional, Union

from .card import AbstractCard, PlayableCharacterCard
from .settings import settings

logger = logging.getLogger("cyberarena.game_module")


class Board:
    """Board Class."""

    def __init__(self) -> None:
        """Constructor."""
        self.__side1: List[PlayableCharacterCard] = []
        self.__nexus1: int = settings.nexus_health
        self.__side2: List[PlayableCharacterCard] = []
        self.__nexus2: int = settings.nexus_health
        self.__boardSize = settings.board_size

    def deploy_card(self, card: AbstractCard, side: int) -> None:
        """
        Deploy a card.

        :param card: Card to deploy.
        :param side: Side of the board the card is being deployed in.
        """
        if not isinstance(card, PlayableCharacterCard):
            # todo: add support for other cards
            return

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
        for card2 in self.__side2:
            logger.debug(card2)

    def attack_card(
        self,
        cardatt: PlayableCharacterCard,
        cardrecv: PlayableCharacterCard,
        side: int,
    ) -> None:
        """
        Attack a card.

        :param cardatt: Card attacking.
        :param cardrecv: Card receiving the attack.
        :param side: Side of the board of the card recving damage.
        """
        if cardatt.already_attacked:
            logger.error("already attacked this turn")
            return
        cardatt.attack_card(cardrecv)
        if not cardrecv.is_alive():
            if side == 1:
                self.__side1.remove(cardrecv)
            else:
                self.__side2.remove(cardrecv)
        if not cardatt.is_alive():
            if side == 1:
                self.__side2.remove(cardatt)
            else:
                self.__side1.remove(cardatt)

    def attack_nexus(self, idatt: int, side: int) -> None:  # noqa: C901
        """
        Attack the nexus.

        :param idatt: Id of the card attacking.
        :param side: Side of the board of the nexus receving damage.
        """
        if side == 2:
            for card in self.__side1:
                if card.id == idatt:
                    if card.already_attacked:
                        logger.error("already attacked this turn")
                        return
                    self.__nexus2 -= card.ap
                    card.already_attacked = True
                    logger.error("nexus1 attacké")
                    return
        else:
            for card2 in self.__side2:
                if card2.id == idatt:
                    if card2.already_attacked:
                        logger.error("already attacked this turn")
                        return
                    self.__nexus1 -= card2.ap
                    card2.already_attacked = True
                    logger.error("nexus2 attacké")
                    return

    def get_nexus_health(self, side: int) -> int:
        """
        Get the health of a nexus.

        :param side: Side of the board of the nexus.
        :return: The health of the nexus.
        """
        if side == 1:
            return self.__nexus1
        return self.__nexus2

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

    def get_card_debug(
        self,
        player: int,
        index: int,
    ) -> Optional[PlayableCharacterCard]:
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

    def get_card_id(self, player: int, id_card: int) -> Optional[PlayableCharacterCard]:
        """
        Get a card by id.

        :param player: Player to get the card from.
        :param id_card: id of the card to get.
        :return: The card.
        """
        if player == 1:
            for card in self.__side1:
                if card.id == id_card:
                    return card
        else:
            for card2 in self.__side2:
                if card2.id == id_card:
                    return card2
        return None

    def end_turn(self, player: int) -> None:
        """
        Next turn.

        :param player: Player ending the turn.
        """
        if player == 1:
            for card in self.__side2:
                card.end_turn()
        else:
            for card2 in self.__side1:
                card2.end_turn()

    def get_updated_card_stats(self, idcard: int) -> Dict[str, Union[str, int]]:
        """
        Get updated card stats.

        :param idcard: Id of the card to get the stats from.
        :return: The updated stats.
        """
        for card in self.__side1:
            if card.id == idcard:
                return card.to_dict()
        for card2 in self.__side2:
            if card2.id == idcard:
                return card2.to_dict()
        return {}
