# flake8: noqa
# import json
import json
import os

import pytest

from cyberarena.game_module.card import factory_card

cards_path = os.path.join("cyberarena", "tests_data", "cards")


@pytest.mark.anyio
async def test_card_constructor_file_not_found() -> None:
    with pytest.raises(FileNotFoundError):
        factory_card.create_card_from_file(
            os.path.join(cards_path, "hiesenberg", "data2.json"),
        )


@pytest.mark.anyio
async def test_card_constructor_invalid_json() -> None:
    with pytest.raises(json.JSONDecodeError):
        factory_card.create_card_from_file(
            os.path.join(cards_path, "invalid", "invalid_json.json"),
        )
