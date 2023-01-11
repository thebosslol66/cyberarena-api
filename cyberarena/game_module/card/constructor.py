import abc
import json
from typing import Any, Dict, List, Optional

from loguru import logger

from .base import AbstractCard
from .playable_character import PlayableCharacterCard


class ConstructorAbstract(metaclass=abc.ABCMeta):
    """
    CardConstructorAbstract class.

    This class is the abstract class for all card constructors.
    It is use for construct card on plate and character.
    """

    OBLIGATORY_ATTRIBUTES: List[str] = ["name"]
    NUMERICAL_ATTRIBUTES: List[str] = []
    OPTIONAL_ATTRIBUTES: List[str] = ["description"]

    def __init__(self) -> None:
        """Constructor."""
        self._name: str = "Unknown"
        self._card: Optional[AbstractCard] = None
        self.json_data: Dict[str, Any] = {}

    @abc.abstractmethod
    def construct(self, filename: str) -> bool:
        """
        Construct a card from a json file.

        :param filename: The json file to load.
        :return: True if the card is constructed, False otherwise.
        """
        self._reset()
        return self._load_json(filename) and self.check_json()

    def check_json(self) -> bool:
        """
        Check the validity of the json file.

        :return: True if the json file is valid, False otherwise.
        """
        self._name = self.json_data.get("name", self._name)
        for attribute in self.OBLIGATORY_ATTRIBUTES:
            if not self._check_obligatory_attribute(attribute):
                return False
        for attribute2 in self.NUMERICAL_ATTRIBUTES:
            if not self._check_numerical_attribute(attribute2):
                return False
        self._check_unrecognized_attribute()
        return True

    def get_card(self) -> Optional[AbstractCard]:
        """
        Get the card cunstucred by the card constructor.

        :return: The card constructed by the card constructor.
        """
        return self._card

    def _reset(self) -> None:
        """Reset the card constructor."""
        self._name = "Unknown"
        self._card = None
        self.json_data = {}

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

    def _warning_message(self, message: str) -> None:
        """
        Send to loguru a warning message.

        :param message: The warning message to log.
        """
        logger.warning(
            f"The card '{self._name}' have a definition warning : {message}",
        )

    def _error_message(self, message: str) -> None:
        """
        Send to loguru an error message.

        :param message: The error message to log.
        """
        logger.error(
            f"The card '{self._name}' have a definition error : {message}",
        )

    def _check_obligatory_attribute(self, attribute: str) -> bool:
        """
        Check the validity of an obligatory attribute.

        Verify if the attribute is present and if it is a string.
        The attribute must not be empty.

        :param attribute: The attribute to check.
        :return: True if the attribute is valid, False otherwise.
        """
        if attribute not in self.json_data:
            self._error_message(f"The attribute '{attribute}' is missing.")
            return False
        if not isinstance(self.json_data[attribute], str):
            self._warning_message(
                f"The attribute '{attribute}' is not a string.",
            )
            return False
        if self.json_data[attribute] == "":
            self._error_message(
                f"The attribute '{attribute}' is empty.",
            )
            return False
        return True

    def _check_numerical_attribute(self, attribute: str) -> bool:
        """
        Checkthe validity of a numerical attribute.

        Verify if the attribute is present and if it is a number.
        It must be a positive number.

        :param attribute: The attribute to check.
        :return: True if the attribute is valid, False otherwise.
        """
        if attribute not in self.json_data:
            self._error_message(f"The attribute '{attribute}' is missing.")
            return False
        if isinstance(self.json_data[attribute], float):
            self.json_data[attribute] = int(self.json_data[attribute])
            self._warning_message(
                f"The attribute '{attribute}' is not an integer. "
                f"It will be rounded to {self.json_data[attribute]}.",
            )
        if not isinstance(self.json_data[attribute], int):
            self._error_message(
                f"The attribute '{attribute}' is not an integer.",
            )
            return False
        if self.json_data[attribute] < 0:
            self._error_message(
                f"The attribute '{attribute}' is negative.",
            )
            return False
        return True

    def _check_unrecognized_attribute(self) -> None:
        """Check if the file contains unused keys. If not use log an info message."""
        all_lists = (
            self.OBLIGATORY_ATTRIBUTES
            + self.NUMERICAL_ATTRIBUTES
            + self.OPTIONAL_ATTRIBUTES
        )
        for attribute in self.json_data.keys():
            if attribute not in all_lists:
                logger.info(
                    f"The card '{self._name}' have a exedent attribute :"
                    f" The attribute '{attribute}' is not recognized.",
                )


class ConstructorPlayableCharacterCard(ConstructorAbstract):
    """CardConstructor class.

    This class is used to generate a card from a json file.
    It can be used to validate a json file.
    """

    NUMERICAL_ATTRIBUTES = [
        "hp",
        "ap",
        "dp",
        "cost",
    ] + ConstructorAbstract.NUMERICAL_ATTRIBUTES
    OBLIGATORY_ATTRIBUTES = [
        "type",
        "rarity",
    ] + ConstructorAbstract.OBLIGATORY_ATTRIBUTES

    def construct(self, filename: str) -> bool:
        """
        Generate a card from a json file.

        Create a playable card from a json file.
        Can be get with get_card() method.

        :param filename: The json file path.
        :return: True if the card is correctly generated.
        """
        if not super().construct(filename):
            return False
        name = self.json_data["name"]
        cost = self.json_data["cost"]
        hp = self.json_data["hp"]
        ap = self.json_data["ap"]
        dp = self.json_data["dp"]
        self._card = PlayableCharacterCard(name, cost, hp, ap, dp)
        return True
