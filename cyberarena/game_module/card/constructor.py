import abc
from typing import Any, Dict, List, Optional, Tuple

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
    NUMERICAL_ATTRIBUTES: List[str] = ["id"]
    OPTIONAL_ATTRIBUTES: List[str] = ["description"]

    def __init__(self) -> None:
        """Constructor."""
        self._name: str = "Unknown"
        self._card_index: int = -1
        self._card: Optional[AbstractCard] = None
        self.json_data: Dict[str, Any] = {}

    @abc.abstractmethod
    def construct(self, json_data: Dict[str, Any]) -> bool:
        """
        Construct a card from a json file.

        :param json_data: The content of a json file card.
        :return: True if the card is constructed, False otherwise.
        """
        self._reset()
        self.json_data = json_data
        self._card_index = self.json_data.get("id", -1)
        return self.check_json()

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

    def get_card(self) -> Tuple[int, Optional[AbstractCard]]:
        """
        Get the card cunstucred by the card constructor.

        :return: The idex of the card and the card constructed by the card constructor.
            If don't exist return -1 and None.
        """
        return self._card_index, self._card

    def _reset(self) -> None:
        """Reset the card constructor."""
        self._name = "Unknown"
        self._card = None
        self.json_data = {}

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

    def construct(self, json_data: Dict[str, Any]) -> bool:
        """
        Generate a card from a json file.

        Create a playable card from a json file.
        Can be get with get_card() method.

        :param json_data: The content of a json file card.
        :return: True if the card is correctly generated.
        """
        if not super().construct(json_data):
            return False
        name = self.json_data["name"]
        cost = self.json_data["cost"]
        hp = self.json_data["hp"]
        ap = self.json_data["ap"]
        dp = self.json_data["dp"]
        self._card = PlayableCharacterCard(name, cost, hp, ap, dp)
        return True


playable_character_card = ConstructorPlayableCharacterCard()
