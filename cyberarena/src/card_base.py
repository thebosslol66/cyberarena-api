import abc
from typing import Any, Dict


class CardAbstract(metaclass=abc.ABCMeta):
    """class CardAbstract."""

    def __init__(self, name: str, cost: int, hp: int, ap: int) -> None:
        """
        Constructor for CardAbstract.

        :param name: Name of the card.
        :param cost: Cost of the card.
        :param hp: Health points of the card.
        :param ap: Attack points of the card.
        """
        self.__name: str = name
        self.__cost: int = cost
        self.__hp: int = hp
        self.__ap: int = ap

    def __str__(self) -> str:
        """
        Return a string representation of the card.

        :return: A string representation of the card.
        """
        return self.name

    def __repr__(self) -> str:
        """
        Return a string representation of the card.

        :return: A string representation of the card.
        """
        return self.name

    @property
    def name(self) -> str:
        """
        Getter for name.

        :return: name.
        """
        return self.__name

    @property
    def cost(self) -> int:
        """
        Getter for cost.

        :return: cost.
        """
        return self.__cost

    @property
    def hp(self) -> int:
        """
        Getter for hp.

        :return: hp.
        """
        return self.__hp

    @property
    def ap(self) -> int:
        """
        Getter for ap.

        :return: The ap of this CardAbstract.
        """
        return self.__ap

    def attack_card(self, card: "CardAbstract") -> None:
        """
        Attack a card.

        :param card: Card to attack.
        """
        CardAbstract._receive_damage(card, self.__ap)  # noqa: WPS437

    def is_alive(self) -> bool:
        """
        Check if the card is alive.

        :return: True if the card is alive, False otherwise.
        """
        return self.__hp > 0

    @classmethod
    @abc.abstractmethod
    def create_card_from_json(cls, json: Dict[str, Any]) -> "CardAbstract":
        """
        Create a card from a json.

        :param json: Json to use.
        """

    def _receive_damage(self, damage: int) -> None:
        """
        Receive damage.

        :param damage: Damage to receive.
        """
        self.__hp -= damage
