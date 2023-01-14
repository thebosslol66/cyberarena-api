# flake8: noqa
import pytest

from cyberarena.game_module.deck import Deck
from cyberarena.game_module.hand import Hand


@pytest.mark.anyio
async def test_hand() -> None:
    """Test hand."""
    deck = Deck()
    hand = Hand(deck)
    assert hand.get_hand_size() == 0
    hand.get_random_card()
    assert hand.get_hand_size() == 1
    hand.use_card_debug(0, 10)
    assert hand.get_hand_size() == 0