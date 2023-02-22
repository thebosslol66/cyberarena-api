import abc
from typing import Dict, Union

from cyberarena.game_module.card.enums import ObjectCardRace, ObjectCardRarity


class AbstractCard(metaclass=abc.ABCMeta):
    """class AbstractCard."""

    id = -1

    def __init__(
        self,
        name: str,
        description: str = "",
        cost: int = 0,
        rarity: ObjectCardRarity = ObjectCardRarity.COMMON,
    ) -> None:
        """
        Constructor for AbstractCard.

        :param name: Name of the card.
        :param description: Description of the card.
        :param cost: Cost of the card.
        :param rarity: Rarity of the card.
        :raises ValueError: If the name is negative or if the cost is negative.
        """
        self._name: str = name
        self._description: str = description
        self._cost: int = cost
        self._rarity: ObjectCardRarity = rarity
        if self._name == "":
            raise ValueError("The name of the card cannot be empty.")
        if self._cost < 0:
            raise ValueError("The cost of the card cannot be negative.")

    @abc.abstractmethod
    def __str__(self) -> str:
        """
        Return a string representation of the card.

        :return: A string representation of the card.
        """
        return "{0} - {1}".format(self.name, self.description)

    @abc.abstractmethod
    def __repr__(self) -> str:
        """
        Return a string representation of the card.

        :return: A string representation of the card.
        """
        return "{0}(name='{1}', description='{2}', cost={3}, rarity={4})".format(
            self.__class__.__name__,
            self.name,
            self.description,
            self.cost,
            self.rarity,
        )

    @property
    def name(self) -> str:
        """
        Getter for name.

        :return: name.
        """
        return self._name

    @property
    def description(self) -> str:
        """
        Getter for description.

        :return: description.
        """
        return self._description

    @property
    def cost(self) -> int:
        """
        Getter for cost.

        :return: cost.
        """
        return self._cost

    @property
    def rarity(self) -> ObjectCardRarity:
        """
        Getter for rarity.

        :return: rarity.
        """
        return self._rarity

    @abc.abstractmethod
    def to_dict(self) -> Dict[str, Union[str, int]]:
        """Getter for json of the card."""


class AbstractCharacterCard(AbstractCard, metaclass=abc.ABCMeta):
    """class AbstractCharacterCard."""

    def __init__(  # noqa: WPS211
        self,
        name: str,
        hp: int,
        ap: int,
        dp: int = 0,
        description: str = "",
        cost: int = 0,
        rarity: ObjectCardRarity = ObjectCardRarity.COMMON,
        race: ObjectCardRace = ObjectCardRace.HUMAN,
    ) -> None:
        """
        Constructor for AbstractCharacterCard.

        :param name: Name of the card.
        :param hp: Health points of the card.
        :param ap: Attack points of the card.
        :param dp: Defense points of the card.
        :param description: Description of the card.
        :param cost: Cost of the card.
        :param rarity: Rarity of the card.
        :param race: The race of the character.
        :raises ValueError: If the hp, ap or dp is negative.
        """
        super().__init__(
            name=name,
            description=description,
            cost=cost,
            rarity=rarity,
        )
        self._hp: int = hp
        self._ap: int = ap
        self._dp: int = dp
        self._race: ObjectCardRace = race
        valuer_error: str = ""
        if self._hp < 0:
            valuer_error = "The hp is negative."
        elif self._ap < 0:
            valuer_error = "The ap is negative."
        elif self._dp < 0:
            valuer_error = "The dp is negative."
        if valuer_error:
            raise ValueError(valuer_error)

    def __str__(self) -> str:
        """
        Return a string representation of the card.

        :return: A string representation of the card.
        """
        return "{0} - HP: {1} - AP: {2} - DP: {3}".format(
            super().__str__(),
            self.hp,
            self.ap,
            self.dp,
        )

    def __repr__(self) -> str:
        """
        Return a string representation of the card.

        :return: A string representation of the card.
        """
        return "{0}, hp={1}, ap={2}, dp={3}')".format(
            super().__repr__()[:-1],
            self.hp,
            self.ap,
            self.dp,
        )

    @property
    def hp(self) -> int:
        """
        Getter for hp.

        :return: hp.
        """
        return self._hp

    @property
    def ap(self) -> int:
        """
        Getter for ap.

        :return: ap.
        """
        return self._ap

    @property
    def dp(self) -> int:
        """
        Getter for dp.

        :return: dp.
        """
        return self._dp

    @property
    def race(self) -> ObjectCardRace:
        """
        Getter for race.

        :return: race.
        """
        return self._race

    def is_alive(self) -> bool:
        """
        Check if the card is alive.

        :return: True if the card is alive, False otherwise.
        """
        return self.hp > 0

    def end_turn(self) -> None:
        """
        This can execute some code when the turn is ended.

        It is usefull to remove effects or kill a car if it can live only for a number
            of turn.
        """

    def attack_card(self, card: "AbstractCharacterCard") -> None:
        """
        Attack a card.

        :param card: The card to attack.
        """
        card._receive_damage(self.ap)

    def _receive_damage(self, damage: int) -> None:
        """
        Receive damage.

        :param damage: The damage to receive.
        """
        if damage > self.dp:
            self._hp -= damage - self.dp
