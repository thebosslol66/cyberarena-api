from .card import AbstractCard, LibraryCard


def get_card_from_id(id_card: int) -> AbstractCard:
    """
    Get a card from its id.

    :param id_card: ID of the card.  # noqa: DAR003
    :return: The card.
    :raise LibraryCardNotFoundError: If the card is not in the library.
    """
    lib = LibraryCard()
    return lib[id_card]


def get_path_card_image(card_id: int, full_card: bool = False) -> str:
    """
    Get the path of the card image.

    :param card_id: ID of the card.
    :param full_card: If True, return the path of card with stats completed.
    :raises NotImplementedError: If the function is not implemented yet.
    """
    raise NotImplementedError("This function is not implemented yet.")
