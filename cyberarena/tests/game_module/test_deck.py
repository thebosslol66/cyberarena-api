from loguru import logger

from cyberarena.game_module.card.playable_character import PlayableCharacterCard
from cyberarena.game_module.deck import Deck


def test_create_deck() -> None:
    """Test create deck."""
    deck = Deck()
    assert deck is not None
    assert len(deck) == 24
    card = deck.get_random_card()
    assert card is not None
    assert isinstance(card, PlayableCharacterCard)
    card.id = 0
    dict = card.to_dict()
    assert dict is not None
    logger.error(dict)
