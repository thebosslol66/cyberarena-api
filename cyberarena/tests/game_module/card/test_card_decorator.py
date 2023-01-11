# flake8: noqa
import pytest

from cyberarena.game_module.card import PlayableCharacterCard, boost


@pytest.fixture
async def default_card() -> PlayableCharacterCard:
    return PlayableCharacterCard("Cyber-Heisenberg", 1, 1, 1)


######################################################################
#                    TESTS CARD DECORATOR BASIC                      #
######################################################################


@pytest.mark.anyio
@pytest.mark.skip(reason="Not implemented yet")
async def test_card_decorator_cant_use_on_object() -> None:
    pass


######################################################################
#                 TESTS CARD DECORATOR HEALTH BOOST                  #
######################################################################


@pytest.mark.anyio
async def test_card_decorator_health_boost_health_modification(
    default_card: PlayableCharacterCard,
) -> None:
    new_card = boost.DecoratorHealthBoost(default_card, 10)
    assert new_card.hp == 11
    assert new_card.ap == 1
    assert new_card.cost == 1
    assert new_card.dp == 0


@pytest.mark.anyio
async def test_card_decorator_health_boost_attack_modification(
    default_card: PlayableCharacterCard,
) -> None:
    new_card = boost.DecoratorHealthBoost(default_card, 10)
    new_card2 = PlayableCharacterCard("Cyber-Heisenberg", 1, 1, 1)
    new_card2.attack_card(new_card)
    assert new_card.hp == 10
    assert new_card.ap == 1
    assert new_card.cost == 1
    assert new_card.dp == 0
    assert new_card.is_alive() is True


@pytest.mark.anyio
async def test_card_decorator_health_boost_attack_modification_killed(
    default_card: PlayableCharacterCard,
) -> None:
    new_card = boost.DecoratorHealthBoost(default_card, 10)
    new_card2 = PlayableCharacterCard("Cyber-Heisenberg", 1, 1, 11)
    new_card2.attack_card(new_card)
    assert new_card.hp == 0
    assert new_card.ap == 1
    assert new_card.cost == 1
    assert new_card.dp == 0
    assert new_card.is_alive() is False


@pytest.mark.anyio
async def test_card_decorator_health_boost_refresh_ref(
    default_card: PlayableCharacterCard,
) -> None:
    new_card = boost.DecoratorHealthBoost(default_card, 10)
    assert new_card.refresh_card_reference() == new_card


@pytest.mark.anyio
async def test_card_decorator_health_boost_refresh_ref_useless_decorator(
    default_card: PlayableCharacterCard,
) -> None:
    new_card = boost.DecoratorHealthBoost(default_card, 0)
    assert new_card.refresh_card_reference() == default_card


######################################################################
#                TESTS CARD DECORATOR DEFENSE BOOST                  #
######################################################################


@pytest.mark.anyio
async def test_card_decorator_defense_boost_defense_modification(
    default_card: PlayableCharacterCard,
) -> None:
    new_card = boost.DecoratorDefenseBoost(default_card, 10)
    assert new_card.hp == 1
    assert new_card.ap == 1
    assert new_card.cost == 1
    assert new_card.dp == 10


@pytest.mark.anyio
async def test_card_decorator_defense_boost_attack_modification(
    default_card: PlayableCharacterCard,
) -> None:
    new_card = boost.DecoratorDefenseBoost(default_card, 10)
    new_card2 = PlayableCharacterCard("Cyber-Heisenberg", 1, 1, 1)
    new_card2.attack_card(new_card)
    assert new_card.hp == 1
    assert new_card.ap == 1
    assert new_card.cost == 1
    assert new_card.dp == 10
    assert new_card.is_alive() is True


@pytest.mark.anyio
async def test_card_decorator_defense_boost_attack_modification_killed(
    default_card: PlayableCharacterCard,
) -> None:
    new_card = boost.DecoratorDefenseBoost(default_card, 10)
    new_card2 = PlayableCharacterCard("Cyber-Heisenberg", 1, 1, 11)
    new_card2.attack_card(new_card)
    assert new_card.hp == 0
    assert new_card.ap == 1
    assert new_card.cost == 1
    assert new_card.dp == 10
    assert new_card.is_alive() is False


@pytest.mark.anyio
async def test_card_decorator_defense_boost_refresh_ref(
    default_card: PlayableCharacterCard,
) -> None:
    new_card = boost.DecoratorDefenseBoost(default_card, 10)
    assert new_card.refresh_card_reference() == new_card


@pytest.mark.anyio
async def test_card_decorator_defense_boost_refresh_ref_useless_decorator(
    default_card: PlayableCharacterCard,
) -> None:
    new_card = boost.DecoratorDefenseBoost(default_card, 0)
    assert new_card.refresh_card_reference() == default_card


######################################################################
#         TESTS CARD DECORATOR TEMPORARY HIT DEFENSE BOOST           #
######################################################################


@pytest.mark.anyio
async def test_card_decorator_temporary_hit_defense_boost_defense_modification(
    default_card: PlayableCharacterCard,
) -> None:
    new_card = boost.DecoratorTemporaryHitDefenseBoost(default_card, 10)
    assert new_card.hp == 1
    assert new_card.ap == 1
    assert new_card.cost == 1
    assert new_card.dp == 10


@pytest.mark.anyio
async def test_card_decorator_temporary_hit_defense_boost_attack_modification(
    default_card: PlayableCharacterCard,
) -> None:
    new_card = boost.DecoratorTemporaryHitDefenseBoost(default_card, 10)
    new_card2 = PlayableCharacterCard("Cyber-Heisenberg", 1, 1, 1)
    new_card2.attack_card(new_card)
    assert new_card.hp == 1
    assert new_card.ap == 1
    assert new_card.cost == 1
    assert new_card.dp == 9
    assert new_card.is_alive() is True


@pytest.mark.anyio
async def test_card_decorator_temporary_hit_defense_boost_attack_modification_killed(
    default_card: PlayableCharacterCard,
) -> None:
    new_card = boost.DecoratorTemporaryHitDefenseBoost(default_card, 10)
    new_card2 = PlayableCharacterCard("Cyber-Heisenberg", 1, 1, 11)
    new_card2.attack_card(new_card)
    assert new_card.hp == 0
    assert new_card.ap == 1
    assert new_card.cost == 1
    assert new_card.dp == 0
    assert new_card.is_alive() is False


@pytest.mark.anyio
async def test_card_decorator_temporary_hit_defense_boost_refresh_ref(
    default_card: PlayableCharacterCard,
) -> None:
    new_card = boost.DecoratorTemporaryHitDefenseBoost(default_card, 10)
    assert new_card.refresh_card_reference() == new_card


@pytest.mark.anyio
async def test_card_decorator_temporary_hit_defense_boost_refresh_ref_useless_decorator(
    default_card: PlayableCharacterCard,
) -> None:
    new_card = boost.DecoratorTemporaryHitDefenseBoost(default_card, 0)
    assert new_card.refresh_card_reference() == default_card


######################################################################
#        TESTS CARD DECORATOR TEMPORARY TURN DEFENSE BOOST           #
######################################################################


@pytest.mark.anyio
async def test_card_decorator_temporary_turn_defense_boost_defense_modification(
    default_card: PlayableCharacterCard,
) -> None:
    new_card = boost.DecoratorTemporaryTurnDefenseBoost(default_card, 10, 1)
    assert new_card.hp == 1
    assert new_card.ap == 1
    assert new_card.cost == 1
    assert new_card.dp == 10


@pytest.mark.anyio
async def test_card_decorator_temporary_turn_defense_boost_attack_modification(
    default_card: PlayableCharacterCard,
) -> None:
    new_card = boost.DecoratorTemporaryTurnDefenseBoost(default_card, 10, 1)
    new_card2 = PlayableCharacterCard("Cyber-Heisenberg", 1, 1, 1)
    new_card2.attack_card(new_card)
    assert new_card.hp == 1
    assert new_card.ap == 1
    assert new_card.cost == 1
    assert new_card.dp == 10
    assert new_card.is_alive() is True


@pytest.mark.anyio
async def test_card_decorator_temporary_turn_defense_boost_attack_modification_killed(
    default_card: PlayableCharacterCard,
) -> None:
    new_card = boost.DecoratorTemporaryTurnDefenseBoost(default_card, 10, 1)
    new_card2 = PlayableCharacterCard("Cyber-Heisenberg", 1, 1, 11)
    new_card2.attack_card(new_card)
    assert new_card.hp == 0
    assert new_card.ap == 1
    assert new_card.cost == 1
    assert new_card.dp == 10
    assert new_card.is_alive() is False


@pytest.mark.anyio
async def test_card_decorator_temporary_turn_defense_boost_refresh_ref(
    default_card: PlayableCharacterCard,
) -> None:
    new_card = boost.DecoratorTemporaryTurnDefenseBoost(default_card, 10, 1)
    assert new_card.refresh_card_reference() == new_card


@pytest.mark.anyio
async def test_card_decorator_temporary_turn_defense_boost_refresh_ref_useles_decorator(
    default_card: PlayableCharacterCard,
) -> None:
    new_card = boost.DecoratorTemporaryTurnDefenseBoost(default_card, 0, 1)
    assert new_card.refresh_card_reference() == default_card


@pytest.mark.anyio
async def test_card_decorator_temporary_turn_defense_boost_end_turn(
    default_card: PlayableCharacterCard,
) -> None:
    new_card = boost.DecoratorTemporaryTurnDefenseBoost(default_card, 10, 1)
    new_card.end_turn()
    assert new_card.hp == 1
    assert new_card.ap == 1
    assert new_card.cost == 1
    assert new_card.dp == 0
    assert new_card.is_alive() is True
    assert new_card.refresh_card_reference() == default_card


######################################################################
#        TESTS CARD DECORATOR TEMPORARY TURN ATTACK BOOST            #
######################################################################


@pytest.mark.anyio
async def test_card_decorator_temporary_turn_attack_boost_ap_modification(
    default_card: PlayableCharacterCard,
) -> None:
    new_card = boost.DecoratorTemporaryTurnAttackBoost(default_card, 10, 1)
    assert new_card.hp == 1
    assert new_card.ap == 11
    assert new_card.cost == 1
    assert new_card.dp == 0


@pytest.mark.anyio
async def test_card_decorator_temporary_turn_attack_boost_attack_modification(
    default_card: PlayableCharacterCard,
) -> None:
    new_card = boost.DecoratorTemporaryTurnAttackBoost(default_card, 10, 1)
    new_card2 = PlayableCharacterCard("Cyber-Heisenberg", 1, 12, 1)
    new_card.attack_card(new_card2)
    print(new_card, new_card.ap)
    assert new_card2.hp == 1
    assert new_card2.ap == 1
    assert new_card2.cost == 1
    assert new_card2.dp == 0
    assert new_card2.is_alive() is True


@pytest.mark.anyio
async def test_card_decorator_temporary_turn_attack_boost_refresh_ref(
    default_card: PlayableCharacterCard,
) -> None:
    new_card = boost.DecoratorTemporaryTurnAttackBoost(default_card, 10, 1)
    assert new_card.refresh_card_reference() == new_card


@pytest.mark.anyio
async def test_card_decorator_temporary_turn_attack_boost_refresh_ref_useless_decorator(
    default_card: PlayableCharacterCard,
) -> None:
    new_card = boost.DecoratorTemporaryTurnAttackBoost(default_card, 0, 1)
    assert new_card.refresh_card_reference() == default_card


@pytest.mark.anyio
async def test_card_decorator_temporary_turn_attack_boost_end_turn(
    default_card: PlayableCharacterCard,
) -> None:
    new_card = boost.DecoratorTemporaryTurnAttackBoost(default_card, 10, 1)
    new_card.end_turn()
    assert new_card.hp == 1
    assert new_card.ap == 1
    assert new_card.cost == 1
    assert new_card.dp == 0
    assert new_card.is_alive() is True
    assert new_card.refresh_card_reference() == default_card
