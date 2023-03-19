from loguru import logger

from cyberarena.game_module.card import LibraryCard
from cyberarena.game_module.deck import Deck
from cyberarena.game_module.settings import settings


def test_create_deck() -> None:
    """Test create deck."""
    deck = Deck()
    assert deck is not None
    assert len(deck) == 26
    tab = []
    for _ in range(0, 26):
        card = deck.get_random_card()
        assert card is not None
        tab.append(card.id_pic)
    for i in range(0, 13):
        assert tab.__contains__(i)
    for i in range(0, tab.__len__()):
        assert tab[i] in range(0, 13)


def test_verify_creation_with_library() -> None:
    """Test verify creation with library."""
    LibraryCard(
        settings.card_path,
        settings.card_data_filename,
        settings.card_image_filename,
    )
    deck = Deck(True)
    card = deck.get_random_card()
    assert card is not None
    logger.error(card.to_dict())
    card = deck.get_random_card()
    assert card is not None
    logger.error(card.to_dict())
    card = deck.get_random_card()
    assert card is not None
    logger.error(card.to_dict())
    assert 0 == 1
