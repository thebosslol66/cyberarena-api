from typing import List, Optional

from .card import LibraryCard
from .deck import Deck
from .exceptions import GameNotFoundError
from .game import Game
from .player import Player
from .settings import settings


class GameManager:
    """Game Manager Class."""

    def __init__(self) -> None:
        """Constructor."""
        self.__games: List[Game] = []
        self.__players: List[Player] = []
        self.idgames = 0

    @staticmethod
    def set_up_library() -> None:
        """Set up the library."""
        LibraryCard(
            settings.card_path,
            settings.card_data_filename,
            settings.card_image_filename,
        )

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

    def __contains__(self, idgame: int) -> bool:
        """
        Check if a game and a player are in the game manager.

        :param idgame: Id of the game.

        :return: True if player is in the game, False otherwise.
        """
        for game in self.__games:
            if game.id == idgame:
                return True
        return False

    def __len__(self) -> int:
        """
        Get the number of active games.

        :return: The number of active games
        """
        return len(self.__games)

    def __getitem__(self, idgame: int) -> Game:
        """
        Get a game.

        :param idgame: Id of the game.
        :return: The game.
        :raises GameNotFoundError: If the game is not found.
        """
        for game in self.__games:
            if game.id == idgame:
                return game
        raise GameNotFoundError("Game not found")

    def get_game(self, idgame: int) -> Optional[Game]:
        """
        Get a game.

        :param idgame: Id of the game.
        :return: The game.
        """
        try:
            return self[idgame]
        except GameNotFoundError:
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

    def find_game(self, idgame: int) -> Optional[Game]:
        """
        Finds a game from its id.

        :param idgame: Id of the game.
        :return: The game.
        """
        for game in self.__games:
            if game.id == idgame:
                return game
        return None

    def find_player(self, idplayer: int) -> int:
        """
        Finds a player from its id.

        :param idplayer: Id of the player.
        :return: The id of the game current played.
        """
        for game in self.__games:
            if idplayer in game:
                return game.id
        return -1

    def deploy_card(self, idgame: int, idplayer: int, idcard: int) -> None:
        """
        Deploy a card.

        :param idgame: Id of the game.
        :param idplayer: Id of the player.
        :param idcard: Id of the card.
        """
        game = self.find_game(idgame)
        if game:
            if game.player1.id == idplayer:
                game.deploy_card_id(game.player1, idcard)
            if game.player2.id == idplayer:
                game.deploy_card_id(game.player2, idcard)

    def attack_card(self, idgame: int, idplayer: int, idatt: int, idrecv: int) -> None:
        """
        Attack a card.

        :param idgame: Id of the game
        :param idplayer: Id of the player
        :param idatt: ID of the card that attacks
        :param idrecv: ID of the card that suffers the attack
        """
        game = self.find_game(idgame)
        if game:
            if game.player1.id == idplayer:
                game.attack_card_id(game.player1, idatt, idrecv)
            if game.player2.id == idplayer:
                game.attack_card_id(game.player2, idatt, idrecv)

    def get_turn(self, idgame: int) -> int:
        """
        Get the turn of a game.

        :param idgame: Id of the game.
        :return: The turn of the game.
        """
        game = self.find_game(idgame)
        if game:
            if game.check_turn(game.player1):
                return game.player1.id
            return game.player2.id
        return -1


game_manager = GameManager()
