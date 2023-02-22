import logging
from typing import Optional

from .board import Board
from .card import AbstractCard, PlayableCharacterCard
from .player import Player

logger = logging.getLogger("cyberarena.game_module")


class Game:
    """Game Class."""

    def __init__(self, p1: Player, p2: Player) -> None:
        """Constructor.

        :param p1: Player 1.
        :param p2: Player 2.
        """
        self.player1 = p1
        self.player2 = p2
        self.player2.idcardcurr = 100
        self.turn = 1
        self.__board = Board()
        self.id = -1
        self.p1connected = False
        self.p2connected = False

    def __contains__(self, id_player: int) -> bool:
        """
        Check if a player is in the game.

        :param id_player: Id of the player.
        :return: True if player is in the game, False otherwise.
        """
        return id_player in {self.player1.id, self.player2.id}

    def deploy_card(self, player: Player, card: AbstractCard) -> None:
        """
        Deploy a card.

        :param player: Player deploying the card.
        :param card: Card to deploy.
        """
        if not self.check_turn(player):
            logger.debug("It's not your turn!")
            return
        cardrcv = player.use_card(card)
        if cardrcv is None:
            logger.debug("cost too high")
            return
        if player == self.player1:
            self.__board.deploy_card(cardrcv, 1)
        else:
            self.__board.deploy_card(cardrcv, 2)

    def deploy_card_debug(self, player: Player, index: int) -> None:
        """
        Deploy a card debug mode.

        :param player: Player deploying the card.
        :param index: Index of the card to get.
        """
        card = player.use_card_debug(index)
        if card is None:
            logger.debug("cost too high")
            return
        if player == self.player1:
            self.__board.deploy_card(card, 1)
        else:
            self.__board.deploy_card(card, 2)

    def deploy_card_id(self, player: Player, idcard: int) -> None:
        """
        Deploy a card by id.

        :param player: Player deploying the card.
        :param idcard: id of the card to deploy.
        """
        card = player.get_card_from_hand_id(idcard)
        if card is None:
            logger.debug("card doesnt exist")
            return
        self.deploy_card(player, card)

    def attack_card(
        self,
        player: Player,
        cardatt: PlayableCharacterCard,
        cardrecv: PlayableCharacterCard,
    ) -> None:
        """
        Attack a card.

        :param player: Player attacking the card.
        :param cardatt: Card attacking.
        :param cardrecv: Card receiving the attack.
        """
        if not self.check_turn(player):
            logger.debug("It's not your turn!")
            return
        if player == self.player1:
            self.__board.attack_card(cardatt, cardrecv, 2)
        else:
            self.__board.attack_card(cardatt, cardrecv, 1)

    def attack_card_debug(self, player: Player, indexatt: int, indexrecv: int) -> None:
        """
        Attack a card debug mode.

        :param player: Player attacking the card.
        :param indexatt: Index of the card attacking.
        :param indexrecv: Index of the card receiving the attack.
        """
        if player == self.player1:
            cardatt = self.__board.get_card_debug(1, indexatt)
            cardrecv = self.__board.get_card_debug(2, indexrecv)
        else:
            cardatt = self.__board.get_card_debug(2, indexatt)
            cardrecv = self.__board.get_card_debug(1, indexrecv)
        if cardatt is None:
            logger.debug("cardatt doesnt exist")
            return
        if cardrecv is None:
            logger.debug("cardrecv doesnt exist")
            return
        self.attack_card(player, cardatt, cardrecv)

    def attack_card_id(self, player: Player, idatt: int, idrecv: int) -> None:
        """
        Attack a card by id.

        :param player: Player attacking the card.
        :param idatt: id of the card attacking.
        :param idrecv: id of the card receiving the attack.
        """
        if player == self.player1:
            cardatt = self.__board.get_card_id(1, idatt)
            cardrecv = self.__board.get_card_id(2, idrecv)
        else:
            cardatt = self.__board.get_card_id(2, idatt)
            cardrecv = self.__board.get_card_id(1, idrecv)
        if cardatt is None:
            logger.debug("cardatt doesnt exist")
            return
        if cardrecv is None:
            logger.debug("cardrecv doesnt exist")
            return
        self.attack_card(player, cardatt, cardrecv)

    def draw_card(self, player: Player) -> Optional[AbstractCard]:
        """
        Draw a card.

        :param player: Player drawing the card.
        :return: The card drawn.
        """
        if self.check_turn(player):
            return player.draw_card()
        return None

    def get_board(self) -> Board:
        """
        Get the board.

        :return: The board.
        """
        return self.__board

    def check_turn(self, player: Player) -> bool:
        """
        Check the turn.

        :param player: Player to check.
        :return: The turn.
        """
        if self.turn % 2 == 0:
            return player != self.player1
        return player != self.player2

    def increase_turn_debug(self) -> None:
        """Debug increase turn."""
        player = 2 if self.turn % 2 == 0 else 1
        if player == 1:
            self.player1.next_turn()
        else:
            self.player2.next_turn()
        self.turn += 1
        self.__board.end_turn(player)

    def increase_turn(self, idplayer: int) -> None:
        """
        Increase turn.

        :param idplayer: id of the player.
        """
        if idplayer == self.player1.id:
            if not self.check_turn(self.player1):
                return
        if idplayer == self.player2.id:
            if not self.check_turn(self.player2):
                return
        self.increase_turn_debug()

    def get_id(self) -> int:
        """
        Get the game id.

        :return: The game id.
        """
        return self.id
