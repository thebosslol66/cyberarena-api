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
    assert not 0 in game_manager
    game = game_manager.create_game(1, 2, deck1, deck2)
    assert 0 in game_manager


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
async def test_game_manager_get_game_inexistant() -> None:
    game_manager = GameManager()
    assert game_manager.get_game(0) is None


@pytest.mark.anyio
async def test_game_manager_end_game() -> None:
    """Tests if the game is ended."""
    game_manager = GameManager()
    deck1 = Deck()
    deck2 = Deck()
    game = game_manager.create_game(1, 2, deck1, deck2)
    assert game_manager.end_game(game.id)


@pytest.mark.anyio
async def test_game_manager_end_game_inexistant() -> None:
    """Tests if the game is ended."""
    game_manager = GameManager()
    assert not game_manager.end_game(0)


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


@pytest.mark.anyio
async def test_game_manager_draw_card() -> None:
    """Tests if drawing a card works."""
    game_manager = GameManager()
    deck1 = Deck()
    deck2 = Deck()
    game = game_manager.create_game(1, 2, deck1, deck2)
    game.player1.draw_card()
    game.player1.increase_mana(10)
    game_manager.deploy_card(game.id, 1, 0)
    game.get_board().get_board_size() == 1


@pytest.mark.anyio
async def test_game_manager_attack_card() -> None:
    """Tests if attacking a card works."""
    game_manager = GameManager()
    deck1 = Deck()
    deck2 = Deck()
    game = game_manager.create_game(1, 2, deck1, deck2)
    game_manager.draw_card(game.id, 1)
    game.player1.increase_mana(10)
    game_manager.deploy_card(game.id, 1, 0)
    game_manager.next_turn(game.id, 1)
    game_manager.draw_card(game.id, 2)
    game.player2.increase_mana(10)
    game_manager.deploy_card(game.id, 2, 0)
    game_manager.next_turn(game.id, 2)
    game_manager.attack_card(game.id, 1, 0, 0)
    assert game.get_board().get_board_size() == 1


@pytest.mark.anyio
async def test_game_manager_find_player() -> None:
    """Tests if finding a player works."""
    game_manager = GameManager()
    deck1 = Deck()
    deck2 = Deck()
    game = game_manager.create_game(1, 2, deck1, deck2)
    assert game_manager.find_player(1) == 0
    assert game_manager.find_player(2) == 0


@pytest.mark.anyio
async def test_game_manager_find_player_inexistant() -> None:
    """Tests if finding a player works."""
    game_manager = GameManager()
    deck1 = Deck()
    deck2 = Deck()
    game_manager.create_game(1, 2, deck1, deck2)
    assert game_manager.find_player(3) == -1


@pytest.mark.anyio
async def test_game_manager_find_player_multiple_games() -> None:
    """Tests if finding a player works."""
    game_manager = GameManager()
    deck1 = Deck()
    deck2 = Deck()
    game_manager.create_game(1, 2, deck1, deck2)
    game_manager.create_game(3, 4, deck1, deck2)
    assert game_manager.find_player(1) == 0
    assert game_manager.find_player(2) == 0
    assert game_manager.find_player(3) == 1
    assert game_manager.find_player(4) == 1
