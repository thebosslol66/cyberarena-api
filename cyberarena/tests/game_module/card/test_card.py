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
async def test_card_empty_name() -> None:
    """Test card."""
    with pytest.raises(ValueError):
        PlayableCharacterCard("", 1, 1, 1)


@pytest.mark.anyio
async def test_card_negative_cost() -> None:
    """Test card."""
    with pytest.raises(ValueError):
        PlayableCharacterCard("Cyber-Heisenberg", -1, 1, 1)


@pytest.mark.anyio
async def test_card_negative_health() -> None:
    """Test card."""
    with pytest.raises(ValueError):
        PlayableCharacterCard("Cyber-Heisenberg", 1, -1, 1)


@pytest.mark.anyio
async def test_card_negative_attack() -> None:
    """Test card."""
    with pytest.raises(ValueError):
        PlayableCharacterCard("Cyber-Heisenberg", 1, 1, -1)


@pytest.mark.anyio
async def test_card_negative_defense() -> None:
    """Test card."""
    with pytest.raises(ValueError):
        PlayableCharacterCard("Cyber-Heisenberg", 1, 1, 1, dp=-1)
