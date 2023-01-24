from typing import List, Optional

from cyberarena.game_module.deck import Deck
from cyberarena.game_module.game import Game
from cyberarena.game_module.player import Player


class GameManager:
    """Game Manager Class."""

    idgames = 0

    def __init__(self) -> None:
        """Constructor."""
        self.__games: List[Game] = []
        self.__players: List[Player] = []

    def create_game(self, p1id: int, p2id: int, d1: Deck, d2: Deck) -> Game:
        """
        Create a game.

        :param p1id: Player 1 id.
        :param p2id: Player 2 id.
        :param d1: Deck 1.
        :param d2: Deck 2.
        :return: The game created.
        """
        p1 = Player()
        p2 = Player()
        p1.id = p1id
        p2.id = p2id
        p1.change_deck(d1)
        p2.change_deck(d2)
        self.__players.append(p1)
        self.__players.append(p2)
        game = Game(p1, p2)
        game.id = self.idgames
        self.idgames += 1
        self.__games.append(game)
        return game

    def __contains__(self, idgame: int, idplayer: int) -> bool:
        """
        Check if a game and a player are in the game manager.

        :param idgame: Id of the game.
        :param idplayer: Id of the player.

        :return: True if player is in the game, False otherwise.
        """
        for game in self.__games:
            if game.id == idgame:
                if game.player1.id == idplayer or game.player2.id == idplayer:
                    return True
        return False

    def deploy_card(self, idgame: int, idplayer: int, idcard: int) -> None:
        """
        Deploy a card.

        :param idgame: Id of the game.
        :param idplayer: Id of the player.
        :param idcard: Id of the card.
        :return: The card deployed.
        """
        for game in self.__games:
            if game.id == idgame:
                if game.player1.id == idplayer:
                    game.deploy_card_id(game.player1, idcard)
                if game.player2.id == idplayer:
                    game.deploy_card_id(game.player2, idcard)
        return None

    def get_game(self, idgame: int) -> Optional[Game]:
        """
        Get a game.

        :param idgame: Id of the game.
        :return: The game.
        """
        for game in self.__games:
            if game.id == idgame:
                return game
        return None

    def end_game(self, idgame: int) -> bool:
        """
        End a game.

        :param idgame: Id of the game.
        :return: True if the game has been ended, False otherwise.
        """
        for game in self.__games:
            if game.id == idgame:
                self.__games.remove(game)
                return True
        return False
