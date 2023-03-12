from cyberarena.game_module.deck import Deck


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
