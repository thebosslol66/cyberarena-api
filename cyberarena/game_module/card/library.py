import os
from typing import Any, Dict, Generator, List, Optional

from loguru import logger

from ..exceptions import LibraryFileNotFoundError  # noqa: WPS300
from .base import AbstractCard  # noqa: WPS300
from .constructor import ConstructorPlayableCharacterCard  # noqa: WPS300


class Library(object):
    """
    Store all cards in RAM.

    Singleton for optimise the space in RAM
    """

    __instance: Optional["Library"] = None

    def __new__(cls, *args: List[Any], **kwargs: Dict[str, Any]) -> "Library":
        """
        Create the instance if it does not exist.

        :return: The instance of the library.
        :param args: The arguments of the constructor.
        :param kwargs:
            The keyword arguments of the constructor.
            See below.

        :Keyword Arguments:
            * *path_name* (``str``) --
                The path to the folder containing the cards.
            * *default_filename* (``str``) --
                The filename in folder containing data of cards

        """
        if Library.__instance is None:
            logger.debug("Instanciate the singleton Library.")
            Library.__instance = super().__new__(cls)
        return Library.__instance

    def __init__(
        self,
        path_name: str = "",
        default_filename: str = "data.json",
    ) -> None:
        """Virtually private constructor.

        Warning: For the moment, only the first instance is keep in memory

        :param path_name: The path to the library.
        :param default_filename: The default filename of the card.
        :raises LibraryFileNotFoundError:
            If the library path not Exist.
        """
        if Library.__instance is not None:
            return
        self.__library: List[AbstractCard] = []
        self.__library_path = path_name
        self.__default_filename = default_filename
        if not os.path.isdir(self.__library_path):
            logger.error(
                "The path to the library is not a directory: {0}",
                self.__library_path,
            )
            raise LibraryFileNotFoundError(
                f"The library path is not valid: '{path_name}'",
            )
        self.__load_library()

    def __get_cards_path(self) -> Generator[str, None, None]:
        """
        Get each cards in a specific directory.

        Generator of card datafile in the configured path.

        :yield: The path of the card data file.
        """
        for card_dir in os.listdir(self.__library_path):
            is_file = os.path.isfile(
                os.path.join(
                    self.__library_path,
                    card_dir,
                    self.__default_filename,
                ),
            )
            if is_file:
                yield os.path.join(self.__library_path, card_dir)
            else:
                logger.warning(
                    "The card '{0}' does not have a data file '{1}'.",
                    card_dir,
                    self.__default_filename,
                )

    def __load_library(self) -> None:
        """Load all cards in the library."""
        constructor_playable = ConstructorPlayableCharacterCard()
        for card_data in self.__get_cards_path():
            # TODO: Load the card in the correct constructor
            constructor_playable.construct(card_data)
