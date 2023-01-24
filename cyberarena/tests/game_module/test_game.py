# flake8: noqa
import pytest

from cyberarena.game_module.card.playable_character import PlayableCharacterCard
from cyberarena.game_module.game import Game
from cyberarena.game_module.player import Player
from cyberarena.game_module.settings import settings


@pytest.mark.anyio
async def test_init() -> None:
    """Test Init Game."""
    player1 = Player("Heisenberg")
    player2 = Player("Walter")
    assert player1.name == "Heisenberg"
    assert player2.name == "Walter"
    assert player1.life == 20
    assert player2.life == 20
    assert player1.mana == 0
    assert player2.mana == 0
    assert player1.mana_max == 10
    assert player2.mana_max == 10
    game = Game(player1, player2)
    assert game.player1.name == "Heisenberg"
    assert game.player2.name == "Walter"
    assert game.player1.life == 20
    assert game.player2.life == 20
    assert game.player1.mana == 0
    assert game.player2.mana == 0
    assert game.player1.mana_max == 10
    assert game.player2.mana_max == 10
    assert len(game.player1.debug_get_deck()) == settings.deck_size
    assert len(game.player2.debug_get_deck()) == settings.deck_size
    assert len(game.player1.debug_get_hand()) == 0
    assert len(game.player2.debug_get_hand()) == 0


@pytest.mark.anyio
async def test_use_card_values() -> None:
    """Test use card."""
    player1 = Player("Heisenberg")
    player2 = Player("Walter")
    game = Game(player1, player2)
    game.player1.increase_mana(10)
    assert len(game.player1.debug_get_hand()) == 0
    assert len(game.player2.debug_get_hand()) == 0
    game.player1.draw_card()
    assert len(game.player1.debug_get_hand()) == 1
    assert len(game.player2.debug_get_hand()) == 0
    game.player1.use_card_debug(0)
    assert game.player1.mana == 9
    assert len(game.player1.debug_get_hand()) == 0
    assert len(game.player2.debug_get_hand()) == 0
    assert len(game.player1.debug_get_deck()) == (settings.deck_size - 1)
    assert len(game.player2.debug_get_deck()) == settings.deck_size


@pytest.mark.anyio
async def test_use_card_board() -> None:
    """Test use card."""
    player1 = Player("Heisenberg")
    player2 = Player("Walter")
    game = Game(player1, player2)
    game.player1.increase_mana(10)
    assert len(game.player1.debug_get_hand()) == 0
    assert len(game.player2.debug_get_hand()) == 0
    game.player1.draw_card()
    game.deploy_card_debug(game.player1, 0)
    assert game.player1.mana == 9
    assert len(game.player1.debug_get_hand()) == 0
    assert len(game.player2.debug_get_hand()) == 0
    assert game.get_board().get_board_size() == 1
    card = game.get_board().get_card_debug(1, 0)
    assert isinstance(card, PlayableCharacterCard)
    assert card.name == "Cyber-Heisenberg"
    assert card.cost == 1
    assert card.hp == 1
    assert card.ap == 1


@pytest.mark.anyio
async def test_game_p1_attacks_p2() -> None:
    """Test p1 attack p2's card."""
    player1 = Player("Heisenberg")
    player2 = Player("Jessie")
    game = Game(player1, player2)
    game.player1.increase_mana(10)
    game.player2.increase_mana(10)
    game.player1.draw_card()
    game.deploy_card_debug(game.player1, 0)
    game.player2.draw_card()
    game.deploy_card_debug(game.player2, 0)
    assert game.get_board().get_board_size() == 2
    game.attack_card_debug(player1, 0, 0)
    assert game.get_board().get_board_size() == 1


@pytest.mark.anyio
async def test_game_p2_attacks_p1() -> None:
    """Test p2 attack p1's card."""
    player1 = Player("Heisenberg")
    player2 = Player("Jessie")
    game = Game(player1, player2)
    game.player1.increase_mana(10)
    game.player2.increase_mana(10)
    game.player1.draw_card()
    game.deploy_card_debug(game.player1, 0)
    game.player2.draw_card()
    game.deploy_card_debug(game.player2, 0)
    assert game.get_board().get_board_size() == 2
    game.increase_turn_debug()
    game.attack_card_debug(player2, 0, 0)
    assert game.get_board().get_board_size() == 1


@pytest.mark.anyio
async def test_game_p1_attacks_p2_2cardseach() -> None:
    """Test p1 attack p2's card."""
    player1 = Player("Heisenberg")
    player2 = Player("Jessie")
    game = Game(player1, player2)
    game.player1.increase_mana(10)
    game.player2.increase_mana(10)
    game.player1.draw_card()
    game.deploy_card_debug(game.player1, 0)
    game.player2.draw_card()
    game.deploy_card_debug(game.player2, 0)
    game.player1.draw_card()
    game.deploy_card_debug(game.player1, 0)
    game.player2.draw_card()
    game.deploy_card_debug(game.player2, 0)
    assert game.get_board().get_board_size() == 4
    game.attack_card_debug(player1, 0, 0)
    assert game.get_board().get_board_size() == 3


@pytest.mark.anyio
async def test_game_p2_attacks_p1_2cardseach() -> None:
    """Test p2 attack p1's card."""
    player1 = Player("Heisenberg")
    player2 = Player("Jessie")
    game = Game(player1, player2)
    game.player1.increase_mana(10)
    game.player2.increase_mana(10)
    game.player1.draw_card()
    game.deploy_card_debug(game.player1, 0)
    game.player2.draw_card()
    game.deploy_card_debug(game.player2, 0)
    game.player1.draw_card()
    game.deploy_card_debug(game.player1, 0)
    game.player2.draw_card()
    game.deploy_card_debug(game.player2, 0)
    assert game.get_board().get_board_size() == 4
    game.increase_turn_debug()
    game.attack_card_debug(player2, 0, 0)
    assert game.get_board().get_board_size() == 3


@pytest.mark.anyio
async def test_game_p1_attacks_p2_card2hp() -> None:
    """Test p1 attack p2's card."""
    player1 = Player("Heisenberg")
    player2 = Player("Jessie")
    game = Game(player1, player2)
    game.player1.increase_mana(10)
    game.player2.increase_mana(10)
    card = PlayableCharacterCard("Cyber-Heisenberg", 1, 2, 1, 0, "test")
    game.player1.cheat_add_card_to_hand(card)
    game.deploy_card_debug(game.player1, 0)
    card = PlayableCharacterCard("Cyber-Jessie", 1, 2, 1, 0, "test")
    game.player2.cheat_add_card_to_hand(card)
    game.deploy_card_debug(game.player2, 0)
    assert game.get_board().get_board_size() == 2
    game.attack_card_debug(player1, 0, 0)
    game.increase_turn_debug()
    assert game.get_board().get_board_size() == 2
    game.increase_turn_debug()
    game.attack_card_debug(player1, 0, 0)
    assert game.get_board().get_board_size() == 1


@pytest.mark.anyio
async def test_game_p2_attacks_p1_card2hp() -> None:
    """Test p2 attack p1's card."""
    player1 = Player("Heisenberg")
    player2 = Player("Jessie")
    game = Game(player1, player2)
    game.player1.increase_mana(10)
    game.player2.increase_mana(10)
    card = PlayableCharacterCard("Cyber-Heisenberg", 1, 2, 1, 0, "test")
    game.player1.cheat_add_card_to_hand(card)
    game.deploy_card_debug(game.player1, 0)
    card = PlayableCharacterCard("Cyber-Jessie", 1, 2, 1, 0, "test")
    game.player2.cheat_add_card_to_hand(card)
    game.deploy_card_debug(game.player2, 0)
    assert game.get_board().get_board_size() == 2
    game.increase_turn_debug()
    game.attack_card_debug(player2, 0, 0)
    game.increase_turn_debug()
    assert game.get_board().get_board_size() == 2
    game.increase_turn_debug()
    game.attack_card_debug(player2, 0, 0)
    assert game.get_board().get_board_size() == 1


@pytest.mark.anyio
async def test_game_board_filling() -> None:
    """Test board filling."""
    player1 = Player("Heisenberg")
    player2 = Player("Jessie")
    game = Game(player1, player2)
    game.player1.increase_mana(10)
    game.player2.increase_mana(10)
    for _ in range(5):
        game.player1.draw_card()
        game.deploy_card_debug(game.player1, 0)
        game.player2.draw_card()
        game.deploy_card_debug(game.player2, 0)
    assert game.get_board().get_board_size() == 10
    game.player1.draw_card()
    game.deploy_card_debug(game.player1, 0)
    assert game.get_board().get_board_size() == 10


@pytest.mark.anyio
async def test_game_turns() -> None:
    """Test turns."""
    player1 = Player("Heisenberg")
    player2 = Player("Jessie")
    game = Game(player1, player2)
    assert game.check_turn(player1) is True
    assert game.check_turn(player2) is False
    game.increase_turn_debug()
    assert game.check_turn(player1) is False
    assert game.check_turn(player2) is True
    game.increase_turn_debug()
    assert game.check_turn(player1) is True
    assert game.check_turn(player2) is False


@pytest.mark.anyio
async def test_game_card_id_is_correct() -> None:
    """Test if cards id are set correctly"""
    player1 = Player("Heisenberg")
    player2 = Player("Jessie")
    game = Game(player1, player2)
    assert game.player1.idcard == 0
    assert game.player2.idcard == 100


@pytest.mark.anyio
async def test_game_card_id_is_correct_p1_use_cheat_add() -> None:
    """Test if cards id are set correctly"""
    player1 = Player("Heisenberg")
    player2 = Player("Jessie")
    game = Game(player1, player2)
    game.player1.increase_mana(10)
    card = PlayableCharacterCard("Cyber-Heisenberg", 1, 2, 1, 0, "test")
    game.player1.cheat_add_card_to_hand(card)
    game.deploy_card_debug(game.player1, 0)
    assert game.get_board().get_card_debug(1, 0).id == 0


@pytest.mark.anyio
async def test_game_card_id_is_correct_p2_use_cheat_add() -> None:
    """Test if cards id are set correctly"""
    player1 = Player("Heisenberg")
    player2 = Player("Jessie")
    game = Game(player1, player2)
    game.player2.increase_mana(10)
    game.increase_turn_debug()
    card = PlayableCharacterCard("Cyber-Heisenberg", 1, 2, 1, 0, "test")
    game.player2.cheat_add_card_to_hand(card)
    game.deploy_card_debug(game.player2, 0)
    assert game.get_board().get_card_debug(2, 0).id == 100


@pytest.mark.anyio
async def test_game_card_id_is_correct_p1_use_draw() -> None:
    """Test if cards id are set correctly"""
    player1 = Player("Heisenberg")
    player2 = Player("Jessie")
    game = Game(player1, player2)
    game.player1.increase_mana(10)
    game.player1.draw_card()
    game.deploy_card_debug(game.player1, 0)
    assert game.get_board().get_card_debug(1, 0).id == 0


@pytest.mark.anyio
async def test_game_card_id_is_correct_p2_use_draw() -> None:
    """Test if cards id are set correctly"""
    player1 = Player("Heisenberg")
    player2 = Player("Jessie")
    game = Game(player1, player2)
    game.player2.increase_mana(10)
    game.increase_turn_debug()
    game.player2.draw_card()
    game.deploy_card_debug(game.player2, 0)
    assert game.get_board().get_card_debug(2, 0).id == 100


@pytest.mark.anyio
async def test_game_card_id_is_correct_multiple_cards_p1() -> None:
    """Test if cards id are set correctly"""
    player1 = Player("Heisenberg")
    player2 = Player("Jessie")
    game = Game(player1, player2)
    game.player1.increase_mana(10)
    game.player1.draw_card()
    game.deploy_card_debug(game.player1, 0)
    assert game.get_board().get_card_debug(1, 0).id == 0
    game.increase_turn_debug()
    game.player1.draw_card()
    game.deploy_card_debug(game.player1, 0)
    assert game.get_board().get_card_debug(1, 1).id == 1
    game.increase_turn_debug()
    game.player1.draw_card()
    game.deploy_card_debug(game.player1, 0)
    assert game.get_board().get_card_debug(1, 2).id == 2
    game.increase_turn_debug()
    game.player1.draw_card()
    game.deploy_card_debug(game.player1, 0)
    assert game.get_board().get_card_debug(1, 3).id == 3
    game.increase_turn_debug()
    game.player1.draw_card()
    game.deploy_card_debug(game.player1, 0)
    assert game.get_board().get_card_debug(1, 4).id == 4


@pytest.mark.anyio
async def test_game_card_id_is_correct_multiple_cards_p2() -> None:
    """Test if cards id are set correctly"""
    player1 = Player("Heisenberg")
    player2 = Player("Jessie")
    game = Game(player1, player2)
    game.player2.increase_mana(10)
    game.increase_turn_debug()
    game.player2.draw_card()
    game.deploy_card_debug(game.player2, 0)
    assert game.get_board().get_card_debug(2, 0).id == 100
    game.increase_turn_debug()
    game.player2.draw_card()
    game.deploy_card_debug(game.player2, 0)
    assert game.get_board().get_card_debug(2, 1).id == 101
    game.increase_turn_debug()
    game.player2.draw_card()
    game.deploy_card_debug(game.player2, 0)
    assert game.get_board().get_card_debug(2, 2).id == 102
    game.increase_turn_debug()
    game.player2.draw_card()
    game.deploy_card_debug(game.player2, 0)
    assert game.get_board().get_card_debug(2, 3).id == 103
    game.increase_turn_debug()
    game.player2.draw_card()
    game.deploy_card_debug(game.player2, 0)
    assert game.get_board().get_card_debug(2, 4).id == 104


@pytest.mark.anyio
async def test_game_card_id_is_correct_multiple_cards_cross_test() -> None:
    """Test if cards id are set correctly"""
    player1 = Player("Heisenberg")
    player2 = Player("Jessie")
    game = Game(player1, player2)
    game.player1.increase_mana(10)
    game.player2.increase_mana(10)
    game.player1.draw_card()
    game.deploy_card_debug(game.player1, 0)
    assert game.get_board().get_card_debug(1, 0).id == 0
    game.increase_turn_debug()
    game.player2.draw_card()
    game.deploy_card_debug(game.player2, 0)
    assert game.get_board().get_card_debug(2, 0).id == 100
    game.increase_turn_debug()
    game.player1.draw_card()
    game.deploy_card_debug(game.player1, 0)
    assert game.get_board().get_card_debug(1, 1).id == 1
    game.increase_turn_debug()
    game.player2.draw_card()
    game.deploy_card_debug(game.player2, 0)
    assert game.get_board().get_card_debug(2, 1).id == 101
    game.increase_turn_debug()
    game.player1.draw_card()
    game.deploy_card_debug(game.player1, 0)
    assert game.get_board().get_card_debug(1, 2).id == 2
    game.increase_turn_debug()
    game.player2.draw_card()
    game.deploy_card_debug(game.player2, 0)
    assert game.get_board().get_card_debug(2, 2).id == 102


@pytest.mark.anyio
async def test_game_card_id_deploy_correct() -> None:
    """Test if cards id are set correctly"""
    player1 = Player("Heisenberg")
    player2 = Player("Jessie")
    game = Game(player1, player2)
    game.player1.increase_mana(10)
    card = PlayableCharacterCard("Cyber-Heisenberg", 1, 2, 1, 0, "test")
    game.player1.cheat_add_card_to_hand(card)
    game.deploy_card_id(player1, 0)
    assert game.get_board().get_board_size() == 1


@pytest.mark.anyio
async def test_game_card_id_deploy_incorrect() -> None:
    """Test if cards id are set correctly"""
    player1 = Player("Heisenberg")
    player2 = Player("Jessie")
    game = Game(player1, player2)
    game.player1.increase_mana(10)
    card = PlayableCharacterCard("Cyber-Heisenberg", 1, 2, 1, 0, "test")
    game.player1.cheat_add_card_to_hand(card)
    game.deploy_card_id(player1, 1)
    assert game.get_board().get_board_size() == 0


@pytest.mark.anyio
async def test_game_card_id_attack_valid() -> None:
    """Test if cards id are set correctly"""
    player1 = Player("Heisenberg")
    player2 = Player("Jessie")
    game = Game(player1, player2)
    game.player1.increase_mana(10)
    card = PlayableCharacterCard("Cyber-Heisenberg", 1, 2, 1, 0, "test")
    game.player1.cheat_add_card_to_hand(card)
    game.deploy_card_id(player1, 0)
    game.player2.increase_mana(10)
    card = PlayableCharacterCard("Cyber-Jessie", 1, 1, 1, 0, "test")
    game.player2.cheat_add_card_to_hand(card)
    game.deploy_card_id(player2, 100)
    game.attack_card_id(player1, 0, 100)
    assert game.get_board().get_board_size() == 1


@pytest.mark.anyio
async def test_game_card_id_attack_invalid_cardrecv() -> None:
    """Test if cards id are set correctly"""
    player1 = Player("Heisenberg")
    player2 = Player("Jessie")
    game = Game(player1, player2)
    game.player1.increase_mana(10)
    card = PlayableCharacterCard("Cyber-Heisenberg", 1, 2, 1, 0, "test")
    game.player1.cheat_add_card_to_hand(card)
    game.deploy_card_id(player1, 0)
    game.player2.increase_mana(10)
    card = PlayableCharacterCard("Cyber-Jessie", 1, 1, 1, 0, "test")
    game.player2.cheat_add_card_to_hand(card)
    game.deploy_card_id(player2, 100)
    game.attack_card_id(player1, 0, 101)
    assert game.get_board().get_board_size() == 2


@pytest.mark.anyio
async def test_game_card_id_attack_invalid_cardatt() -> None:
    """Test if cards id are set correctly"""
    player1 = Player("Heisenberg")
    player2 = Player("Jessie")
    game = Game(player1, player2)
    game.player1.increase_mana(10)
    card = PlayableCharacterCard("Cyber-Heisenberg", 1, 2, 1, 0, "test")
    game.player1.cheat_add_card_to_hand(card)
    game.deploy_card_id(player1, 0)
    game.player2.increase_mana(10)
    card = PlayableCharacterCard("Cyber-Jessie", 1, 1, 1, 0, "test")
    game.player2.cheat_add_card_to_hand(card)
    game.deploy_card_id(player2, 100)
    game.attack_card_id(player1, 1, 100)
    assert game.get_board().get_board_size() == 2
