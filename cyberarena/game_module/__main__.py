# pragma: no cover

import argparse
import logging
import os

from cyberarena.game_module.card.library import Library
from cyberarena.game_module.image_card_generator import (
    ImageCardGenerator,
    is_data_or_image_newer_than_builded_card,
)
from cyberarena.game_module.settings import settings

logger = logging.getLogger("cyberarena.game_module")
FORMAT = (
    "%(asctime)-15s | %(levelname)s | "  # noqa: WPS323
    "%(module)s:%(funcName)s:%(lineno)d - %(message)s"  # noqa: WPS323
)
logging.Formatter(FORMAT, style="%")
logging.basicConfig(format=FORMAT, level=logging.WARNING)

logger_validator = logging.getLogger("cyberarena.game_module.card_validator")
logger_generator = logging.getLogger("cyberarena.game_module.image_generator")
logger_generator.disabled = True


def verify_library(folder: str) -> None:
    """
    Verify the syntax of the cards.

    It will check every card in the folder and will print the result of the validation.

    :param folder: The folder containing all the different cards.
    """
    # Remove the default handler of the logger
    logger_validator.handlers = []
    # Add a new handler to the logger
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(message)s"))  # noqa: WPS323
    logger_validator.addHandler(handler)
    logger_validator.setLevel(logging.DEBUG)
    logger_validator.propagate = False

    lib = Library(
        folder,
        default_filename=settings.card_data_filename,
        default_image=settings.card_image_filename,
    )
    for index in lib:
        logger.info("Card {0} is valid".format(index))


def set_logger_for_generation() -> None:
    """
    Set the logger for the generation of the images.

    It will inactivate the logger for the validation of the cards.
    And it will activate the logger for the generation of the images.
    """
    # Remove the default handler of the logger
    logger_generator.handlers = []
    # Add a new handler to the logger
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(message)s"))  # noqa: WPS323
    logger_generator.addHandler(handler)
    logger_generator.setLevel(logging.INFO)
    logger_generator.propagate = False
    logger_generator.disabled = False

    logger_validator.disabled = True


def is_card_must_be_generated(image_file_path: str, output: str) -> bool:
    """
    Check if the card must be generated.

    It will check if the card is already generated and if the card is
    modified since the last generation.

    :param image_file_path: The path to the image file of the card.
    :param output: The folder where the image is save.
    :return: True if the card must be generated, False otherwise.
    """
    data_file_path = image_file_path.replace(
        settings.card_image_filename,
        settings.card_data_filename,
    )
    return is_data_or_image_newer_than_builded_card(
        data_file_path,
        image_file_path,
        output,
    )


def generate_and_save_card_images(lib: Library, force: bool) -> None:
    """
    Generate and save the card images.

    It will generate the card images and save them in the output folder.

    :param lib: The library containing the cards.
    :param force: Force the generation of the image.
    """
    output = ImageCardGenerator.resources.output_folder
    image_nb = 0
    for index in lib.keys():
        image_nb += 1
        must_be_gnerated = is_card_must_be_generated(
            lib.get_img_path(index),
            os.path.join(
                output,
                "{0}.png".format(index),
            ),
        )
        if not must_be_gnerated and not force:
            logger_generator.info(
                "Skip image for card {0}, {1}/{2}".format(
                    lib[index].name,
                    image_nb,
                    len(lib),
                ),
            )
            continue
        logger_generator.info(
            "Generate image for card {0}, {1}/{2}".format(
                lib[index].name,
                image_nb,
                len(lib),
            ),
        )
        generator = ImageCardGenerator(
            lib[index],
            lib.get_img_path(index),
        )
        generator.generate_card()
        generator.save_image("{0}.png".format(index))


def create_image(folder: str, output: str, force: bool) -> None:  # noqa: WPS210
    """
    Create the image of cards.

    Will create the image of the card from input folder to the output folder.
    It will verify the validity of the output directory, if not exist ask the
    user if he want to create it.
    **Warning**: This function will stop the execution if the output folder
    doesn't exist and wait the user confirmation to create it.
    **Warning**: It will overwrite every older card image with the same name if data or
    image is newer than the image card.

    :param folder: The folder containing all the different cards.
    :param output: The folder where the images will be saved.
    :param force: Force the generation of the image.
    """
    set_logger_for_generation()
    lib = Library(
        folder,
        default_filename=settings.card_data_filename,
        default_image=settings.card_image_filename,
    )

    logger_generator.warning(
        "WARNING: Don't forget to verify data"
        " before generate image."
        "\nUse 'python -m cyberarena.game_module verify'.",
    )

    if not os.path.isdir(output):
        validation = None
        while validation != "y":
            validation = input(  # noqa: WPS421
                "Do you want to create the folder ?[{0}] (y/n) ".format(output),
            )
            if validation == "n":
                return
        os.mkdir(output)

    logger_generator.info("Output folder: {0}".format(output))

    ImageCardGenerator.resources.output_folder = output
    generate_and_save_card_images(lib, force)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Card library manager",
        description="This program generate all cards image for the game."
        "It use the syntax of the same template for all cards.",
        add_help=True,
    )

    subparser = parser.add_subparsers(
        help="Operations to do on elements in the library",
        dest="subcommand",
    )

    verify_parser = subparser.add_parser(
        "verify",
        help="Verify the syntax of the cards.",
    )

    construct_parser = subparser.add_parser(
        "create",
        help="Create the image of the cards.",
    )

    parser.add_argument(
        "-v",
        "--version",
        help="Show the version of the program.",
        action="version",
        version="%(prog)s 1.0",  # noqa: WPS323
    )

    verify_parser.add_argument(
        "-d",
        "--directory",
        help="The folder containing all the different cards.",
        type=str,
        required=False,
        dest="directory",
        default="./cyberarena/tests_data/cards",
    )

    construct_parser.add_argument(
        "-d",
        "--directory",
        help="The folder containing all the different cards.",
        type=str,
        required=False,
        dest="directory",
        default="./cyberarena/tests_data/cards",
    )

    construct_parser.add_argument(
        "-o",
        "--output",
        help="The folder where to put the generated images.",
        type=str,
        required=False,
        dest="output",
        default="./cyberarena/tests_data/images",
    )

    construct_parser.add_argument(
        "-f",
        "--force",
        help="Force the generation of the image.",
        required=False,
        dest="force",
        action="store_true",
    )

    args = parser.parse_args()

    if args.subcommand == "verify":
        verify_library(args.directory)
    elif args.subcommand == "create":
        create_image(args.directory, args.output, args.force)
