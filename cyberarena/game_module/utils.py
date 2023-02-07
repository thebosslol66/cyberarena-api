import os

from .card import AbstractCard, LibraryCard
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
    lib = Library()
    card = get_card_from_id(card_id)
    data_file_path = lib.get_img_path(card_id).replace(
        settings.card_image_filename,
        settings.card_data_filename,
    )
    builded_card_filename = os.path.join(
        settings.card_image_path,
        "{0}_static.png".format(card_id),
    )
    if is_data_or_image_newer_than_builded_card(
        data_file_path,
        lib.get_img_path(card_id),
        builded_card_filename,
    ):  # noqa: WPS337
        icg = ImageCardGenerator(card, lib.get_img_path(card_id))
        icg.generate_card()
        icg.save_image_with_values(settings.dynamic_image.format(card_id))


def setup_library() -> None:
    """Set up the library."""
    LibraryCard(
        settings.card_path,
        settings.card_data_filename,
        settings.card_image_filename,
    )


def setup_card_images() -> None:  # noqa: WPS210
    """
    Set up the card images.

    It generates the card images from the card data.
    """
    if not os.path.exists(settings.card_image_path):
        os.makedirs(settings.card_image_path)
    lib = Library()
    for card_id in Library().keys():
        card = get_card_from_id(card_id)
        data_file_path = lib.get_img_path(card_id).replace(
            settings.card_image_filename,
            settings.card_data_filename,
        )
        builded_card_filename = os.path.join(
            settings.card_image_path,
            "{0}_static.png".format(card_id),
        )
        if os.path.exists(builded_card_filename):
            continue
        icg = ImageCardGenerator(card, lib.get_img_path(card_id))
        icg.resources.output_folder = settings.card_image_path
        icg.generate_card()
        if is_data_or_image_newer_than_builded_card(
            data_file_path,
            lib.get_img_path(card_id),
            builded_card_filename,
        ):  # noqa: WPS337
            icg.save_image_with_values(settings.static_image.format(card_id))
            icg.save_image(settings.dynamic_image.format(card_id))


def setup_game_module() -> None:
    """
    Initialize the game module.

    It load the cards in the library and it generates cards images from it.
    """
    setup_library()
    setup_card_images()
