# flake8: noqa
import pytest

from cyberarena.game_module.deck import Deck
from cyberarena.game_module.game_manager import GameManager


@pytest.mark.anyio
async def test_game_manager() -> None:
    """Test game manager."""
    game_manager = GameManager()
    deck1 = Deck()
    deck2 = Deck()
    game = game_manager.create_game(1, 2, deck1, deck2)
    assert game_manager.__contains__(game.id, 1)
    assert game_manager.__contains__(game.id, 2)


@pytest.mark.anyio
async def test_game_manager_get_game() -> None:
    """Test init game."""
    game_manager = GameManager()
    deck1 = Deck()
    deck2 = Deck()
    game = game_manager.create_game(1, 2, deck1, deck2)
    assert game_manager.get_game(game.id) == game
    assert game.player1.id == 1
    assert game.player2.id == 2


@pytest.mark.anyio
async def test_game_manager_get_turn_correct() -> None:
    """Tests if the turn is correct"""
    game_manager = GameManager()
    deck1 = Deck()
    deck2 = Deck()
    game = game_manager.create_game(1, 2, deck1, deck2)
    assert game_manager.get_game(game.id).turn == 1
    assert game_manager.get_turn(game.id) == 1
    game.increase_turn_debug()
    assert game_manager.get_game(game.id).turn == 2
    assert game_manager.get_turn(game.id) == 2


@pytest.mark.anyio
async def test_game_manager_deploy_card() -> None:
    """Tests if deployment of a card works."""
    game_manager = GameManager()
    deck1 = Deck()
    deck2 = Deck()
    game = game_manager.create_game(1, 2, deck1, deck2)
    game.player1.draw_card()
    game.player1.increase_mana(10)
    game_manager.deploy_card(game.id, 1, 0)
    game.get_board().get_board_size() == 1
