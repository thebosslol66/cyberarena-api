import json
from typing import Any, Dict, Optional

from loguru import logger

from .base import AbstractCard
from .constructor import ConstructorAbstract, playable_character_card
from .enums import ObjectCardType


class FactoryCard(object):
    """FactoryCard class."""

    def __init__(self) -> None:
        """Constructor."""
        self.json_data: Optional[Dict[str, Any]] = {}

    def create_card_from_file(self, filename: str) -> Optional[AbstractCard]:
        """
        Create a card from a json file.

        :param filename: The json file to load.
        :return: The card constructed from the json file.
        """
        self.json_data = None
        if not self._load_json(filename) or self.json_data is None:
            return None
        constructor: Optional[ConstructorAbstract] = self._return_constructor()
        if constructor is None:
            return None
        if not constructor.construct(self.json_data):
            return None
        return constructor.get_card()

    def _load_json(self, filename: str) -> bool:
        """
        Load a json file.

        :param filename: The json file to load.
        :return: True if the file is loaded, False otherwise. # noqa: DAR003
        :raises FileNotFoundError: If the file is not found.
        :raise json.JSONDecodeError: If the file is not a json file.
        """
        try:
            with open(filename, "r") as file:
                self.json_data = json.load(file)
            # TODO: replace with module exeption
        except FileNotFoundError as error:
            logger.error(f"The file '{filename}' does not exist.")
            raise error
        except json.JSONDecodeError as error:
            logger.error(f"The file '{filename}' is not a valid json.")
            raise error
        return True

    def _return_constructor(self) -> Optional[ConstructorAbstract]:
        """
        Return the constructor of the card with defined type.

        Warning: the file must be loaded before.

        :return: The constructor of the card with defined type.
        """
        if self.json_data is None:
            return None
        card_type: str = self.json_data.get("card_type", "Unknown")
        if card_type == "Unknown":
            card_name = self.json_data.get("name", "Unknown")
            logger.error(
                f"The card '{card_name}' " "have an undefined type.",
            )
            return None

        possible_return = {
            ObjectCardType.OBJECT: playable_character_card,
            ObjectCardType.CHARACTER: playable_character_card,
            ObjectCardType.PLAYER: playable_character_card,
        }
        return_value = possible_return.get(ObjectCardType(card_type), None)
        if return_value is None:
            card_name = self.json_data.get("name", "Unknown")
            logger.error(
                f"The card '{card_name}' " "have an unrecognized type.",
            )
        return return_value


factory_card = FactoryCard()
