from typing import List

from cyberarena.game_module.card import PlayableCharacterCard
from cyberarena.game_module.settings import settings


class Board:
    """Board Class."""

    def __init__(self) -> None:
        """Constructor."""
        self.__side1: List[PlayableCharacterCard] = []
        self.__side2: List[PlayableCharacterCard] = []
        self.__boardSize = settings.board_size

    def deploy_card(self, card: PlayableCharacterCard, side: int) -> None:
        """
        Deploy a card.

        :param card: Card to deploy.
        :param side: Side of the board the card is being deployed in.
        """
        if side == 1:
            self.__side1.append(card)
        else:
            self.__side2.append(card)

    def show_board(self) -> None:
        """Show the board."""
        print("Side 1:")
        for card in self.__side1:
            print(card)
        print("Side 2:")
        for card in self.__side2:
            print(card)

    def attack_card(self, card: PlayableCharacterCard, side: int) -> None:
        """
        Attack a card.

        :param card: Card to attack.
        :param side: Side of the board the card is being attacked in.
        """
        if side == 1:
            self.__side2.remove(card)
        else:
            self.__side1.remove(card)
