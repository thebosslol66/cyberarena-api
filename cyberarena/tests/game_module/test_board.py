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


@pytest.mark.anyio
async def test_board_attack_card_dead_p1p2() -> None:
    """Test board attack card."""
    board = Board()
    card1 = PlayableCharacterCard("Cyber-Heisenberg", 1, 1, 1, 0, "test")
    card2 = PlayableCharacterCard("Cyber-Jessie", 1, 1, 1, 0, "test")
    board.deploy_card(card1, 1)
    board.deploy_card(card2, 2)
    assert board.get_board_size() == 2
    board.attack_card(card1, card2, 2)
    assert board.get_board_size() == 1


@pytest.mark.anyio
async def test_board_attack_card_dead_p2p1() -> None:
    """Test board attack card."""
    board = Board()
    card1 = PlayableCharacterCard("Cyber-Heisenberg", 1, 1, 1, 0, "test")
    card2 = PlayableCharacterCard("Cyber-Jessie", 1, 1, 1, 0, "test")
    board.deploy_card(card1, 1)
    board.deploy_card(card2, 2)
    assert board.get_board_size() == 2
    board.attack_card(card2, card1, 1)
    assert board.get_board_size() == 1


@pytest.mark.anyio
async def test_attack_nexus() -> None:
    """Test board attack card."""
    board = Board()
    card1 = PlayableCharacterCard("Cyber-Heisenberg", 3, 3, 3, 0, "test")
    card1.id = 0
    board.deploy_card(card1, 1)
    assert board.get_board_size() == 1
    board.attack_nexus(0, 2)
    assert board.get_board_size() == 1
    assert board.get_nexus_health(2) == 97
