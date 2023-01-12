# flake8: noqa
import json
import os

import pytest

from cyberarena.game_module.card import ConstructorPlayableCharacterCard

cards_path = os.path.join("cyberarena", "tests_data", "cards")


@pytest.fixture
def card_constructor() -> ConstructorPlayableCharacterCard:
    return ConstructorPlayableCharacterCard()


def open_json_file(path: str) -> dict:
    with open(path, "r") as file:
        return json.load(file)


######################################################################
#           TESTS CARD CONSTRUCTOR PLAYABLE CHARACTER                #
######################################################################
@pytest.mark.anyio
async def test_card_constructor_default(
    card_constructor: ConstructorPlayableCharacterCard,
) -> None:
    data = open_json_file(os.path.join(cards_path, "hiesenberg", "data.json"))
    assert card_constructor.construct(data) is True
    card = card_constructor.get_card()
    assert card is not None
    assert card.name == "Cyber-Heisenberg"
    assert card.cost == 10
    assert card.hp == 11
    assert card.ap == 13
    assert card.dp == 12


@pytest.mark.parametrize(
    "attribute_name",
    ["type", "rarity", "name"],
)
@pytest.mark.anyio
async def test_card_constructor_no_obligatory_attribute(
    attribute_name: str,
    card_constructor: ConstructorPlayableCharacterCard,
) -> None:
    data = open_json_file(
        os.path.join(cards_path, "invalid", f"no_{attribute_name}.json"),
    )
    assert (
        card_constructor.construct(
            data,
        )
        is False
    )
    assert card_constructor.get_card() is None


@pytest.mark.anyio
async def test_card_constructor_obligatory_attribute_empty(
    card_constructor: ConstructorPlayableCharacterCard,
) -> None:
    data = open_json_file(os.path.join(cards_path, "invalid", "name_empty.json"))
    assert (
        card_constructor.construct(
            data,
        )
        is False
    )
    assert card_constructor.get_card() is None


@pytest.mark.anyio
async def test_card_constructor_obligatory_attribute_is_a_number(
    card_constructor: ConstructorPlayableCharacterCard,
) -> None:
    data = open_json_file(
        os.path.join(cards_path, "invalid", "name_number.json"),
    )
    assert (
        card_constructor.construct(
            data,
        )
        is False
    )
    assert card_constructor.get_card() is None


@pytest.mark.parametrize(
    "attribute_name",
    ["ap", "dp", "hp", "cost"],
)
@pytest.mark.anyio
async def test_card_constructor_no_numerical_attribute(
    attribute_name: str,
    card_constructor: ConstructorPlayableCharacterCard,
) -> None:
    data = open_json_file(
        os.path.join(cards_path, "invalid", f"no_{attribute_name}.json"),
    )
    assert (
        card_constructor.construct(
            data,
        )
        is False
    )
    assert card_constructor.get_card() is None


@pytest.mark.parametrize(
    "attribute_name",
    ["ap", "dp", "hp", "cost"],
)
@pytest.mark.anyio
async def test_card_constructor_invalid_numerical_attribute(
    attribute_name: str,
    card_constructor: ConstructorPlayableCharacterCard,
) -> None:
    data = open_json_file(
        os.path.join(cards_path, "invalid", f"{attribute_name}_not_int.json"),
    )
    assert (
        card_constructor.construct(
            data,
        )
        is False
    )
    assert card_constructor.get_card() is None


@pytest.mark.anyio
async def test_card_constructor_numerical_attribute_is_float(
    card_constructor: ConstructorPlayableCharacterCard,
) -> None:
    data = open_json_file(
        os.path.join(cards_path, "invalid", "hp_is_float.json"),
    )
    assert (
        card_constructor.construct(
            data,
        )
        is True
    )
    assert card_constructor.get_card() is not None
    assert card_constructor.get_card().hp == 11  # TODO: test log output


@pytest.mark.anyio
async def test_card_constructor_numerical_attribute_is_negative(
    card_constructor: ConstructorPlayableCharacterCard,
) -> None:
    data = open_json_file(
        os.path.join(cards_path, "invalid", "hp_is_negative.json"),
    )
    assert (
        card_constructor.construct(
            data,
        )
        is False
    )
    assert card_constructor.get_card() is None


@pytest.mark.anyio
async def test_card_constructor_unused_attribute(
    card_constructor: ConstructorPlayableCharacterCard,
) -> None:
    data = open_json_file(
        os.path.join(cards_path, "invalid", "unused_attribute.json"),
    )
    assert (
        card_constructor.construct(
            data,
        )
        is True
    )
    assert card_constructor.get_card() is not None
