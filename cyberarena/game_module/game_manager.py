from typing import List, Optional

from . import AbstractCard
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

    def __contains__(self, id_game: int) -> bool:
        """
        Check if a game and a player are in the game manager.

        :param id_game: Id of the game.

        :return: True if player is in the game, False otherwise.
        """
        for game in self.__games:
            if game.id == id_game:
                return True
        return False

    def __len__(self) -> int:
        """
        Get the number of active games.

        :return: The number of active games
        """
        return len(self.__games)

    def __getitem__(self, id_game: int) -> Game:
        """
        Get a game.

        :param id_game: Id of the game.
        :return: The game.
        :raises GameNotFoundError: If the game is not found.
        """
        for game in self.__games:
            if game.id == id_game:
                return game
        raise GameNotFoundError("Game not found")

    def get_game(self, id_game: int) -> Optional[Game]:
        """
        Get a game.

        :param id_game: Id of the game.
        :return: The game.
        """
        try:
            return self[id_game]
        except GameNotFoundError:
            return None

    def end_game(self, id_game: int) -> bool:
        """
        End a game.

        :param id_game: Id of the game.
        :return: True if the game has been ended, False otherwise.
        """
        for game in self.__games:
            if game.id == id_game:
                self.__games.remove(game)
                return True
        return False

    def find_game(self, id_game: int) -> Optional[Game]:
        """
        Finds a game from its id.

        :param id_game: Id of the game.
        :return: The game.
        """
        for game in self.__games:
            if game.id == id_game:
                return game
        return None

    def find_player(self, id_player: int) -> int:
        """
        Finds a player from its id.

        :param id_player: Id of the player.
        :return: The id of the game current played.
        """
        for game in reversed(self.__games):
            if game.player1.id == id_player:
                return game.id
            if game.player2.id == id_player:
                return game.id
        return -1

    def draw_card(
        self,
        idgame: int,
        idplayer: int,
        force: bool = False,
    ) -> Optional[AbstractCard]:
        """
        Draw a card.

        :param idgame: Id of the game.
        :param idplayer: Id of the player.
        :param force: Force the draw.
        :return: The card drawn.
        """
        game = self.find_game(idgame)
        if game:
            if game.player1.id == idplayer:
                return game.draw_card(game.player1, force)
            if game.player2.id == idplayer:
                return game.draw_card(game.player2, force)
        return None

    def deploy_card(self, id_game: int, id_player: int, id_card: int) -> int:
        """
        Deploy a card.

        :param id_game: Id of the game.
        :param id_player: Id of the player.
        :param id_card: Id of the card.
        :return: Status of the deployment.
        """
        game = self.find_game(id_game)
        if game:
            if game.player1.id == id_player:
                return game.deploy_card_id(game.player1, id_card)
            if game.player2.id == id_player:
                return game.deploy_card_id(game.player2, id_card)
        return -4

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

    def attack_nexus(self, idgame: int, idplayer: int, idatt: int) -> None:
        """
        Attack the nexus.

        :param idgame: Id of the game
        :param idplayer: Id of the player
        :param idatt: ID of the card that attacks
        """
        game = self.find_game(idgame)
        if game:
            if game.player1.id == idplayer:
                game.attack_nexus(game.player1, idatt)
            if game.player2.id == idplayer:
                game.attack_nexus(game.player2, idatt)

    def get_turn(self, id_game: int) -> int:
        """
        Get the turn of a game.

        :param id_game: Id of the game.
        :return: The turn of the game.
        """
        game = self.find_game(id_game)
        if game:
            if game.check_turn(game.player1):
                return game.player1.id
            return game.player2.id
        return -1

    def connect(self, idgame: int, idplayer: int) -> bool:
        """
        Connect a player to a game.

        :param idgame: Id of the game.
        :param idplayer: Id of the player.
        :return: True if both players are connected, False otherwise.
        """
        game = self.find_game(idgame)
        if game:
            if game.player1.id == idplayer:
                game.p1connected = True
            if game.player2.id == idplayer:
                game.p2connected = True
            if game.p1connected and game.p2connected:
                return True
        return False

    def next_turn(self, idgame: int, idplayer: int) -> None:
        """
        Go to the next turn.

        :param idgame: Id of the game.
        :param idplayer: Id of the player.
        """
        game = self.find_game(idgame)
        if game:
            game.increase_turn(idplayer)


game_manager = GameManager()
