from typing import Optional

from .base import AbstractCard
from .enums import ObjectCardRarity, ObjectCardType


class InfoCard(AbstractCard):
    """CardInfo class."""

    def __init__(  # noqa: WPS211
        self,
        name: str,
        description: str,
        cost: int,
        card_type: ObjectCardType,
        card_rarity: ObjectCardRarity,
    ) -> None:
        """
        Constructor.

        :param name: The name of the card.
        :param description: The description of the card.
        :param cost: The cost of the card.
        :param card_type: The type of the card.
        :param card_rarity: The rarity of the card.

        """
        super().__init__(name, description, cost)
        self._hp: Optional[int] = None
        self._dp: Optional[int] = None
        self._ap: Optional[int] = None
        self._card_type = card_type
        self._card_rarity = card_rarity

    def __str__(self) -> str:
        """
        Return the string representation of the card.

        :return: The string representation of the card.
        """
        return f"{self.name} - {self.description}"

    def __repr__(self) -> str:
        """
        Return the representation of the card.

        :return: The representation of the card.
        """
        return "{0}(name='{1}', description='{2}')".format(
            self.__class__.__name__,
            self.name,
            self.description,
        )

    @property
    def card_type(self) -> ObjectCardType:
        """
        Return the type of the card.

        :return: The type of the card.
        """
        return self._card_type

    @property
    def card_rarity(self) -> ObjectCardRarity:
        """
        Return the rarity of the card.

        :return: The rarity of the card.
        """
        return self._card_rarity

    @property
    def cost(self) -> int:
        """
        Return the cost of the card.

        :return: The cost of the card.
        """
        return self._cost

    @property
    def hp(self) -> Optional[int]:
        """
        Return the hp of the card.

        :return: The hp of the card.
        """
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        """
        Set the hp of the card.

        :param value: The hp of the card.
        """
        self._hp = value

    @property
    def ap(self) -> Optional[int]:
        """
        Return the ap of the card.

        :return: The ap of the card.
        """
        return self._ap

    @ap.setter
    def ap(self, value: int) -> None:
        """
        Set the ap of the card.

        :param value: The ap of the card.
        """
        self._ap = value

    @property
    def dp(self) -> Optional[int]:
        """
        Return the dp of the card.

        :return: The dp of the card.
        """
        return self._dp

    @dp.setter
    def dp(self, value: int) -> None:
        """
        Set the dp of the card.

        :param value: The dp of the card.
        """
        self._dp = value

    @property
    def description(self) -> str:
        """
        Return the description of the card.

        :return: The description of the card.
        """
        return self._description

    @property
    def name(self) -> str:
        """
        Return the name of the card.

        :return: The name of the card.
        """
        return self._name

    @property
    def type(self) -> str:
        """
        Return the type of the card.

        :return: The type of the card.
        """
        return self._card_type

    @property
    def rarity(self) -> str:
        """
        Return the rarity of the card.

        :return: The rarity of the card.
        """
        return self._card_rarity
