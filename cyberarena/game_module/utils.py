import os

from .card import AbstractCard
from .card.library import Library
from .image_card_generator import (
    ImageCardGenerator,
    is_data_or_image_newer_than_builded_card,
)
from .settings import settings


def get_card_from_id(id_card: int) -> AbstractCard:
    """
    Get a card from its id.

    :param id_card: ID of the card.  # noqa: DAR003
    :return: The card.
    :raise LibraryCardNotFoundError: If the card is not in the library.
    """
    lib = Library()
    return lib[id_card]


def get_path_card_image(card_id: int, static: bool = False) -> str:
    """
    Get the path of the card image.

    :param card_id: ID of the card.
    :param static: If True, return the path of card with static stats.
    :return: The path of the card image.
    """
    if static:
        return os.path.join(
            settings.card_image_path,
            settings.static_image.format(card_id),
        )
    return os.path.join(
        settings.card_image_path,
        settings.dynamic_image.format(card_id),
    )


def update_card_image(card_id: int) -> None:
    """
    Update the image of a card.

    :param card_id: ID of the card.
    """
    card = get_card_from_id(card_id)
    if is_data_or_image_newer_than_builded_card("data.json", "0.png", "heisenberg"):
        icg = ImageCardGenerator(card, settings.card_image_path)
        icg.generate_card()
        icg.save_image(settings.static_image.format(card_id))
