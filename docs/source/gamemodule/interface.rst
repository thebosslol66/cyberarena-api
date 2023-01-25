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
- __init__(gameDAO):

  - creates a list of Games
  - creates a list of Players

- create_game(p1id, p2id, deck1, deck2):
  creates a game with the given players's id and decks
  returns the game

- __contains(idgame, idplayer):
  returns True if the player is in the game

- get_game(idgame):
  returns the game

- end_game(idgame):
  ends the game
