# flake8: noqa
import pytest

from cyberarena.game_module.deck import Deck
from cyberarena.game_module.game_manager import GameManager


@pytest.mark.anyio
async def test_game_manager() -> None:
    """Test game manager."""
    game_manager = GameManager()
    player1 = game_manager.create_player("Heisenberg")
    player2 = game_manager.create_player("Walter White")
    deck1 = Deck()
    deck2 = Deck()
    game = game_manager.create_game(player1, player2, deck1, deck2)
    assert game_manager.contains(game.id, player1.id)
    assert game_manager.contains(game.id, player2.id)
    assert not game_manager.contains(0, 0)
    assert not game_manager.contains(game.id, 0)
    assert not game_manager.contains(0, player1.id)
