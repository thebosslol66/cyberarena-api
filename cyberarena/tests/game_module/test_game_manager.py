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
