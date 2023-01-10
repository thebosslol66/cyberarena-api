# flake8: noqa
import pytest as pytest

from cyberarena.game_module.card import PlayableCharacterCard


@pytest.mark.anyio
async def test_card() -> None:
    """Test card."""
    card = PlayableCharacterCard("Cyber-Heisenberg", 1, 1, 1)
    assert card.name == "Cyber-Heisenberg"
    assert card.cost == 1
    assert card.hp == 1
    assert card.ap == 1


@pytest.mark.anyio
async def test_card_attack() -> None:
    """Test card attack."""
    card = PlayableCharacterCard("Cyber-Heisenberg", 1, 1, 1)
    card2 = PlayableCharacterCard("Cyber-Heisenberg", 1, 1, 1)
    card.attack_card(card2)
    assert card2.hp == 0
    assert card2.ap == 1
    assert card2.cost == 1
    assert card2.is_alive() is False

    assert card.hp == 1
    assert card.ap == 1
    assert card.cost == 1
    assert card.is_alive() is True
