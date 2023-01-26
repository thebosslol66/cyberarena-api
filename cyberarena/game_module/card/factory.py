import json
import logging
from typing import Any, Dict, Optional, Tuple

from .base import AbstractCard
from .constructor import ConstructorAbstract, playable_character_card
from .enums import ObjectCardType

logger = logging.getLogger("cyberarena.game_module.card_validator")


class FactoryCard(object):
    """FactoryCard class."""

    def __init__(self) -> None:
        """Constructor."""
        self.json_data: Optional[Dict[str, Any]] = {}

    def create_card_from_file(
        self,
        filename: str,
    ) -> Tuple[int, Optional[AbstractCard]]:
        """
        Create a card from a json file.

        :param filename: The json file to load.
        :return: The index of the card and the card constructed from the json file.
        """
        self.json_data = None
        if not self.load_json(filename) or self.json_data is None:
            return -1, None  # pragma: no cover
        constructor: Optional[ConstructorAbstract] = self._return_constructor()
        self.json_data.pop("card_type", None)
        if constructor is None:
            return -1, None
        if not constructor.construct(self.json_data):
            return -1, None  # pragma: no cover
        return constructor.get_card()

    def load_json(self, filename: str) -> bool:
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
            return None  # pragma: no cover
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
        for key, value in possible_return.items():
            if card_type == str(key):
                return value
        card_name = self.json_data.get("name", "Unknown")
        logger.error(
            f"The card '{card_name}' have an unrecognized type: {card_type}.",
        )
        return None


factory_card = FactoryCard()
