# flake8: noqa
import json
import os
import shutil
from typing import Any, Dict

import pytest

from cyberarena.game_module.card import LibraryCard

CARD_PATH = os.path.join("cyberarena", "tests_data", "cards")


@pytest.fixture(autouse=True)
def remove_invalid_card_folder(
    tmpdir: Any,
) -> None:
    shutil.move(os.path.join(CARD_PATH, "invalid"), os.path.join(tmpdir, "invalid"))
    LibraryCard.reset()
    yield None
    shutil.move(os.path.join(tmpdir, "invalid"), os.path.join(CARD_PATH, "invalid"))


@pytest.fixture
def second_test_card() -> None:
    shutil.copytree(
        os.path.join(CARD_PATH, "hiesenberg"),
        os.path.join(CARD_PATH, "ihiesenberg"),
    )
    yield json.load(open(os.path.join(CARD_PATH, "ihiesenberg", "data.json"), "r"))
    shutil.rmtree(os.path.join(CARD_PATH, "ihiesenberg"))


######################################################################
#                       TESTS CARD LIBRARY                           #
######################################################################


@pytest.mark.anyio
async def test_card_library_singleton() -> None:
    """Test the singleton of the library."""
    library1 = LibraryCard(CARD_PATH)
    library2 = LibraryCard()
    assert library1 is library2


@pytest.mark.anyio
async def test_card_library_list_files() -> None:
    library = LibraryCard(CARD_PATH)
    assert len(library) == len(os.listdir(CARD_PATH)) - 2


@pytest.mark.anyio
async def test_card_library_get_card_path() -> None:
    library = LibraryCard(CARD_PATH)
    assert library.get_img_path(0) == os.path.join(CARD_PATH, "hiesenberg", "card.png")


@pytest.mark.anyio
async def test_card_have_same_id(
    second_test_card: Dict[str, Any],
    caplog: Any,
) -> None:
    second_test_card["name"] = "ihiesenberg"
    with open(os.path.join(CARD_PATH, "ihiesenberg", "data.json"), "w") as f:
        json.dump(second_test_card, f)
    library = LibraryCard(CARD_PATH)
    assert len(library) == len(os.listdir(CARD_PATH)) - 3
    assert library[0].name == "Cyber-Heisenberg"
    assert library.get_img_path(0) == os.path.join(CARD_PATH, "hiesenberg", "card.png")
    assert "2 cards have the same id" in caplog.text
    for record in caplog.records:
        if record.message == "2 cards have the same id":
            assert os.path.join(CARD_PATH, "hiesenberg") in record.message
            assert os.path.join(CARD_PATH, "ihiesenberg") in record.message
            assert record.levelname == "ERROR"


@pytest.mark.anyio
async def test_card_have_same_name(
    second_test_card: Dict[str, Any],
    caplog: Any,
) -> None:
    second_test_card["id"] = 1
    with open(os.path.join(CARD_PATH, "ihiesenberg", "data.json"), "w") as f:
        json.dump(second_test_card, f)
    library = LibraryCard(CARD_PATH)
    assert len(library) == len(os.listdir(CARD_PATH)) - 2
    assert library[0].name == "Cyber-Heisenberg"
    assert library[1].name == "Cyber-Heisenberg"
    assert "The card with name 'Cyber-Heisenberg' already exist" in caplog.text
    for record in caplog.records:
        if record.message == "The card with name 'Cyber-Heisenberg' already exist":
            assert os.path.join(CARD_PATH, "hiesenberg") in record.message
            assert os.path.join(CARD_PATH, "ihiesenberg") in record.message
            assert record.levelname == "WARNING"


# TODO: make test (ex: if type is not written, file not exist etc.)
