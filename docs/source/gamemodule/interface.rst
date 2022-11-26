Interface of game module
========================

This interface will be used to represent a game.
It will implement all mechanisms of the game, included error handler of imposible moves.
This documentation is used to implement the api endpoints and websocket communication
with the game mechanism.

Methods to implement
--------------------


The following functions must be implemented:

- `createGame(gameDAO)` : Create a new game and register it in the database. it return the game id.
- `addPlayer(gameId, gameDAO, playerid)` : Add a player to the game. It returns true if the player was added, false otherwise and logg into console
- `removePlayer(gameId, gameDAO, playerid)` : Remove a player from the game. It returns true if the player was removed, false otherwise and logg into console
- `startGame(gameId, gameDAO)` : Start the game. It returns true if the game was started, false otherwise and log into console

- `isGameStarted(gameId, gameDAO)` : Return true if the game is started, false otherwise
- `isGameFinished(gameId, gameDAO)` : Return true if the game is finished, false otherwise

- `getCurrentPlayer(gameId, gameDAO)` : Return the current player id for specified id
