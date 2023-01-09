# flake8: noqa
import json
import os

import pytest

from cyberarena.src.card_constructor import CardConstructor

cards_path = os.path.join("cyberarena", "tests_data", "cards")


@pytest.fixture
def card_constructor() -> CardConstructor:
    return CardConstructor()


######################################################################
#                     TESTS CARD CONSTRUCTOR                         #
######################################################################
@pytest.mark.anyio
async def test_card_constructor_default(
    card_constructor: CardConstructor,
) -> None:
    assert (
        card_constructor.construct(os.path.join(cards_path, "hiesenberg", "data.json"))
        is True
    )
    card = card_constructor.get_card()
    assert card is not None
    assert card.name == "Cyber-Heisenberg"
    assert card.cost == 10
    assert card.hp == 11
    assert card.ap == 13
    assert card.dp == 12


@pytest.mark.anyio
async def test_card_constructor_file_not_found(
    card_constructor: CardConstructor,
) -> None:
    with pytest.raises(FileNotFoundError):
        card_constructor.construct(os.path.join(cards_path, "hiesenberg", "data2.json"))


@pytest.mark.anyio
async def test_card_constructor_invalid_json(
    card_constructor: CardConstructor,
) -> None:
    with pytest.raises(json.JSONDecodeError):
        card_constructor.construct(
            os.path.join(cards_path, "invalid", "invalid_json.json"),
        )


@pytest.mark.parametrize(
    "attribute_name",
    ["type", "rarity", "name"],
)
@pytest.mark.anyio
async def test_card_constructor_no_obligatory_attribute(
    attribute_name: str,
    card_constructor: CardConstructor,
) -> None:
    assert (
        card_constructor.construct(
            os.path.join(cards_path, "invalid", f"no_{attribute_name}.json"),
        )
        is False
    )
    assert card_constructor.get_card() is None


@pytest.mark.anyio
async def test_card_constructor_no_obligatory_attribute_empty(
    card_constructor: CardConstructor,
) -> None:
    assert (
        card_constructor.construct(
            os.path.join(cards_path, "invalid", "name_empty.json"),
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
    card_constructor: CardConstructor,
) -> None:
    assert (
        card_constructor.construct(
            os.path.join(cards_path, "invalid", f"no_{attribute_name}.json"),
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
    card_constructor: CardConstructor,
) -> None:
    assert (
        card_constructor.construct(
            os.path.join(cards_path, "invalid", f"{attribute_name}_not_int.json"),
        )
        is False
    )
    assert card_constructor.get_card() is None


@pytest.mark.anyio
async def test_card_constructor_numerical_attribute_is_float(
    card_constructor: CardConstructor,
) -> None:
    assert (
        card_constructor.construct(
            os.path.join(cards_path, "invalid", "hp_is_float.json"),
        )
        is True
    )
    assert card_constructor.get_card() is not None
    assert card_constructor.get_card().hp == 11  # TODO: test log output
