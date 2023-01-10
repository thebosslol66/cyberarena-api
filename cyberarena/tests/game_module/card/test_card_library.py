# flake8: noqa
import os
import shutil
from typing import Any

import pytest

from cyberarena.game_module.card import LibraryCard

CARD_PATH = os.path.join("cyberarena", "tests_data", "cards")


@pytest.fixture
def remove_invalid_card_folder(
    tmpdir: Any,
) -> None:
    shutil.move(os.path.join(CARD_PATH, "invalid"), os.path.join(tmpdir, "invalid"))
    yield None
    shutil.move(os.path.join(tmpdir, "invalid"), os.path.join(CARD_PATH, "invalid"))


######################################################################
#                       TESTS CARD LIBRARY                           #
######################################################################


@pytest.mark.anyio
async def test_card_library_singleton(
    remove_invalid_card_folder: None,
) -> None:
    """Test the singleton of the library."""
    library1 = LibraryCard(CARD_PATH)
    library2 = LibraryCard()
    assert library1 is library2


@pytest.mark.anyio
@pytest.mark.skip(reason="Not implemented")
async def test_card_library_list_files(
    remove_invalid_card_folder: None,
) -> None:
    library = LibraryCard(CARD_PATH)
