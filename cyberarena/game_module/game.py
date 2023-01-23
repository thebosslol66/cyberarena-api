from loguru import logger

from cyberarena.game_module.board import Board
from cyberarena.game_module.card import PlayableCharacterCard
from cyberarena.game_module.player import Player


class Game:
    """Game Class."""

    def __init__(self, p1: Player, p2: Player) -> None:
        """Constructor.

        :param p1: Player 1.
        :param p2: Player 2.
        """
        self.player1 = p1
        self.player2 = p2
        self.turn = 1
        self.__board = Board()

    def deploy_card(self, player: Player, card: PlayableCharacterCard) -> None:
        """
        Deploy a card.

        :param player: Player deploying the card.
        :param card: Card to deploy.
        """
        card = player.use_card(card)
        if card.name == "None":
            logger.debug("cost too high")
            return
        if player == self.player1:
            self.__board.deploy_card(card, 1)
        else:
            self.__board.deploy_card(card, 2)

    def deploy_card_debug(self, player: Player, index: int) -> None:
        """
        Deploy a card debug mode.

        :param player: Player deploying the card.
        :param index: Index of the card to get.
        """
        card = player.use_card_debug(index)
        if card.name == "None":
            logger.debug("cost too high")
            return
        if player == self.player1:
            self.__board.deploy_card(card, 1)
        else:
            self.__board.deploy_card(card, 2)

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
            self.turn += 1
        else:
            self.__board.attack_card(cardatt, cardrecv, 1)
            self.turn += 1

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
        self.attack_card(player, cardatt, cardrecv)

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
            if player == self.player1:
                return False
            else:
                return True
        else:
            if player == self.player1:
                return True
            else:
                return False

    def increase_turn_debug(self) -> None:
        """Debug increase turn."""
        self.turn += 1
