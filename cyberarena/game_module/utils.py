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


def generate_card_images() -> None:
    """
    Generate card images.

    It will verify all card and create new images if needed.
    It runs before the application starts.

    :raises NotImplementedError: If the function is not implemented yet.
    """
    raise NotImplementedError("This function is not implemented yet.")


def get_path_card_image() -> str:
    """
    Get the path of the card image.

    :raises NotImplementedError: If the function is not implemented yet.
    """
    raise NotImplementedError("This function is not implemented yet.")
