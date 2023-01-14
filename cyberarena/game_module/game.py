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
        self.p1 = p1
        self.p2 = p2
        self.turn = 1
        self.__board = Board()

    def deploy_card(self, player: Player, card: PlayableCharacterCard) -> None:
        """
        Deploy a card.

        :param player: Player deploying the card.
        :param card: Card to deploy.
        """
        card = player.use_card(card)
        if player == self.p1:
            self.__board.deploy_card(card, 1)
        else:
            self.__board.deploy_card(card, 2)

    def attack_card(self, player: Player, card: PlayableCharacterCard) -> None:
        """
        Attack a card.

        :param player: Player attacking the card.
        :param card: Card to attack.
        """
        if player == self.p1:
            self.__board.attack_card(card, 1)
        else:
            self.__board.attack_card(card, 2)
