# flake8: noqa
import pytest

from cyberarena.game_module.board import Board
from cyberarena.game_module.card.playable_character import PlayableCharacterCard
from cyberarena.game_module.settings import settings


@pytest.mark.anyio
async def test_board_init() -> None:
    """Test board init."""
    board = Board()
    assert board.get_board_size() == 0
    assert board.get_max_board_size() == settings.board_size


@pytest.mark.anyio
async def test_board_deploy_card_side1() -> None:
    """Test board deploy card."""
    board = Board()
    card = PlayableCharacterCard("Cyber-Heisenberg", 1, 1, 1, 0, "test")
    board.deploy_card(card, 1)
    assert board.get_board_size() == 1
    assert board.get_card_debug(1, 0) == card


@pytest.mark.anyio
async def test_board_deploy_card_side2() -> None:
    """Test board deploy card."""
    board = Board()
    card = PlayableCharacterCard("Cyber-Heisenberg", 1, 1, 1, 0, "test")
    board.deploy_card(card, 2)
    assert board.get_board_size() == 1
    assert board.get_card_debug(2, 0) == card
