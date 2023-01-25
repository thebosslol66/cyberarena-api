import os
import typing

from loguru import logger

from ..exceptions import LibraryFileNotFoundError
from .base import AbstractCard
from .factory import factory_card


class Library(object):
    """
    Store all cards in RAM.

    Singleton for optimise the space in RAM
    """

    __instance: typing.Optional["Library"] = None
    __init_flag = False

    def __new__(
        cls,
        *args: typing.List[typing.Any],
        **kwargs: typing.Dict[str, typing.Any],
    ) -> "Library":
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
        if cls.__instance is None:
            logger.debug("Instanciate the singleton Library.")
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(
        self,
        path_name: str = "",
        default_filename: str = "data.json",
        default_image: str = "card.png",
    ) -> None:
        """Virtually private constructor.

        Warning: For the moment, only the first instance is keep in memory

        :param path_name: The path to the library.
        :param default_filename: The default filename of the card.
        :param default_image: The default image of the card.
        :raises LibraryFileNotFoundError:
            If the library path not Exist.
        """
        if Library.__init_flag:
            return
        self.__library: typing.Dict[int, AbstractCard] = {}
        self.__library_card_path: typing.Dict[int, str] = {}
        self.__library_path = path_name
        self.__default_filename = default_filename
        self.__default_image = default_image
        if not os.path.isdir(self.__library_path):
            logger.error(
                "The path to the library is not a directory: {0}",
                self.__library_path,
            )
            raise LibraryFileNotFoundError(
                f"The library path is not valid: '{path_name}'",
            )
        self.__load_library()
        Library.__init_flag = True

    def __iter__(self) -> typing.Iterator[int]:
        """
        Iterate over the library.

        :return: The iterator of the library.
        """
        return iter(self.__library)

    def __len__(self) -> int:
        """
        Return the number of cards in the library.

        :return: The number of cards in the library.
        """
        return len(self.keys())

    def __getitem__(self, key: int) -> AbstractCard:
        """
        Get a card by his name.

        :param key: The name of the card.
        :return: The card if it exist.
        """
        return self.__library[key]

    def __contains__(self, card: typing.Union[int, AbstractCard]) -> bool:
        """
        Check if the card is in the library.

        :param card: The card to check or his name.
        :return: True if the card is in the library.
        """
        if isinstance(card, int):
            return card in self.__library.keys()
        elif isinstance(card, AbstractCard):
            return card in self.__library.values()
        return False

    def keys(self) -> typing.KeysView[int]:
        """
        Return the list of cards in the library.

        :return: a dict_keys object providing a view on Library's keys.
        """
        return self.__library.keys()

    def values(self) -> typing.ValuesView[AbstractCard]:
        """
        Return the list of cards in the library.

        :return: a dict_values object providing a view on Library's values.
        """
        return self.__library.values()

    def items(self) -> typing.ItemsView[int, AbstractCard]:
        """
        Return the list of cards in the library.

        :return: a dict_items object providing a view on Library's items.
        """
        return self.__library.items()

    def get_card_path(self, card_id: int) -> str:
        """
        Return the path of the card image.

        :param card_id: The id of the card.
        :raises KeyError: If the card is not in the library.
        :return: The path of the card image.
        """
        if card_id not in self.__library_card_path:
            logger.error(
                "The card '{0}' is not in the library.",
                card_id,
            )
            raise KeyError(
                f"The card '{card_id}' is not in the library.",
            )
        return self.__library_card_path[card_id]

    def __get_cards_path(self) -> typing.Generator[typing.Tuple[str, str], None, None]:
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
            is_image = os.path.isfile(
                os.path.join(
                    self.__library_path,
                    card_dir,
                    self.__default_image,
                ),
            )
            if is_file and is_image:
                yield os.path.join(
                    self.__library_path,
                    card_dir,
                    self.__default_filename,
                ), os.path.join(
                    self.__library_path,
                    card_dir,
                    self.__default_image,
                )
            else:
                logger.warning(
                    "The card '{0}' does not have a data file '{1}'.",
                    card_dir,
                    self.__default_filename,
                )

    def __load_library(self) -> None:
        """Load all cards in the library."""
        for (card_data, card_img) in self.__get_cards_path():
            (card_id, card) = factory_card.create_card_from_file(card_data)
            if card is not None:
                self.__library[card_id] = card
                self.__library_card_path[card_id] = card_img
