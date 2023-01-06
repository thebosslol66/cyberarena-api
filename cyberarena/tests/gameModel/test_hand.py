import pytest as pytest

from cyberarena.src.deck import Deck
from cyberarena.src.hand import Hand


@pytest.mark.anyio
async def test_hand() -> None:
    """Test hand."""
    deck = Deck()
    hand = Hand(deck)
    assert hand.get_hand_size() == 0
    hand.get_random_card()
    assert hand.get_hand_size() == 1