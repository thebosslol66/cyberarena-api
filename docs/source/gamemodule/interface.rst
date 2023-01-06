Interface of game module
########################

What is needed to be done
=========================

This interface will represent a game and implement all of its mechanisms,
including error handling for impossible moves.
It will be used to implement API endpoints and websocket
communication with the game mechanism.

Design Patterns to be used
==========================

- Singleton:
    For storing game cards  in memory

- Monteur ou fabrique:
    For creating cards of games

- Decorateur:
    For effects applied to cards.
    For example, a card can be a "card with a shield" or a card poisoned.


Methods to Implement
=====================
- createGame(gameDAO):

  - Creates a new game and registers it in the database.
  - Returns the game's ID.

- addPlayer(gameId, gameDAO, playerId):

  - Adds a player to the game.
  - Returns true if the player was added, false otherwise.
  - Logs any errors to the console.

- removePlayer(gameId, gameDAO, playerId):

  - Removes a player from the game.
  - Returns true if the player was removed, false otherwise.
  - Logs any errors to the console.

- startGame(gameId, gameDAO):

  - Starts the game.
  - Returns true if the game was started, false otherwise.
  - Logs any errors to the console.

- isGameStarted(gameId, gameDAO):

  - Returns true if the game has started, false otherwise.

- isGameFinished(gameId, gameDAO):

  - Returns true if the game has finished, false otherwise.

- getCurrentPlayer(gameId, gameDAO):

  - Returns the ID of the current player for the specified game.
