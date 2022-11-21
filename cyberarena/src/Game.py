import logging
LOGGER = logging.getLogger("game")
class Game:
    def __init__(self, id, player1, player2, terrain) -> None:
        self.player1 = player1
        self.player2 = player2
        self.board = terrain
        self.turn = 0
        self.winner = None
        self.id = id

    def play(self) -> None:
        while self.winner is None:
            self.turn += 1
            if self.turn % 2 == 1:
                self.player1.play(self.board)
            else:
                self.player2.play(self.board)
            self.winner = self.board.check_winner()

    def print_winner(self) -> None:
        if self.winner is None:
            LOGGER.debug("No winner")
        else:
            LOGGER.debug(self.winner.name + " won the game")

    def __str__(self) -> str:
        return (
            "Game between "
            + self.player1.name
            + " and "
            + self.player2.name
            + " on "
            + self.board.name
        )
