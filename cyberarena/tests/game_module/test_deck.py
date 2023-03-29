from loguru import logger

from cyberarena.game_module.card import LibraryCard
from cyberarena.game_module.deck import Deck
from cyberarena.game_module.settings import settings


def test_verify_creation_with_library() -> None:
    """Test verify creation with library."""
    LibraryCard(
        settings.card_path,
        settings.card_data_filename,
        settings.card_image_filename,
    )
    deck = Deck()
    for _ in range(0, 26):
        card = deck.get_random_card()
        assert card is not None
        logger.error(card.to_dict())
