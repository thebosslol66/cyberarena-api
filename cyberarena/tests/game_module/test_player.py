import pytest as pytest

from cyberarena.game_module.card.base import AbstractCard
from cyberarena.game_module.player import Player


@pytest.mark.anyio
async def test_player() -> None:
    """Test player."""
    player = Player("Heisenberg")
    assert player.name == "Heisenberg"
    assert player.life == 20
    assert player.mana == 0
    player.increase_mana(10)
    assert player.mana == 10
    player.increase_mana(10)
    assert player.mana == 10


@pytest.mark.anyio
async def test_player_use_cost_is_correct() -> None:
    """Test player card is correct."""
    player = Player("Heisenberg")
    player.increase_mana(10)
    player.draw_card()
    player.use_card_debug(0)
    assert player.mana == 9


@pytest.mark.anyio
async def test_player_use_hp_is_correct() -> None:
    """Test player card is correct."""
    player = Player("Heisenberg")
    player.increase_mana(10)
    player.draw_card()
    card: AbstractCard = player.use_card_debug(0)
    assert card.hp == 1


@pytest.mark.anyio
async def test_player_use_ap_is_correct() -> None:
    """Test player card is correct."""
    player = Player("Heisenberg")
    player.increase_mana(10)
    player.draw_card()
    card: AbstractCard = player.use_card_debug(0)
    assert card.ap == 1


@pytest.mark.anyio
async def test_player_use_name_is_correct() -> None:
    """Test player card is correct."""
    player = Player("Heisenberg")
    player.increase_mana(10)
    player.draw_card()
    card: AbstractCard = player.use_card_debug(0)
    assert card.name == "Cyber-Heisenberg"


@pytest.mark.anyio
async def test_player_use_card_cost_too_high() -> None:
    """Test player card is correct."""
    player = Player("Heisenberg")
    player.draw_card()
    card = player.use_card_debug(0)
    assert card.name == "None"
