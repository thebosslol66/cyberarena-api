import argparse
import logging

from cyberarena.game_module.card.library import Library
from cyberarena.game_module.image_card_generator import ImageCardGenerator

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

    lib = Library(folder)
    for index in lib:
        logger.info("Card {0} is valid".format(index))


def create_image(folder: str) -> None:
    """
    Create the image of the cards.

    :param folder: The folder containing all the different cards.
    """
    # Remove the default handler of the logger
    logger_generator.handlers = []
    # Add a new handler to the logger
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(message)s"))  # noqa: WPS323
    logger_generator.addHandler(handler)
    logger_generator.setLevel(logging.DEBUG)
    logger_generator.propagate = False
    logger_generator.disabled = False

    logger_validator.disabled = True
    lib = Library(folder, is_image_info=True)

    logger_generator.warning(
        "WARNING: Don't forget to verify data"
        " before generate image."
        "\nUse 'python -m game_module verify'.",
    )

    image_nb = 0
    for index in lib.keys():
        image_nb += 1
        logger_generator.info(
            "Generate image for card {0}, {1}/{2}".format(
                lib[index].name,
                image_nb,
                len(lib),
            ),
        )
        generator = ImageCardGenerator(
            lib[index],  # type: ignore
            lib.get_img_path(index),
        )
        generator.generate_card().show()


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

    args = parser.parse_args()

    if args.subcommand == "verify":
        verify_library(args.directory)
    elif args.subcommand == "create":
        create_image(args.directory)
