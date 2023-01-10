import abc


class AbstractCard(metaclass=abc.ABCMeta):
    """class AbstractCard."""

    def __init__(self, name: str, description: str = "") -> None:
        """
        Constructor for AbstractCard.

        :param name: Name of the card.
        :param description: Description of the card.
        """
        self._name: str = name
        self._description: str = description

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
        return "{0}(name='{1}', description='{2}')".format(
            self.__class__.__name__,
            self.name,
            self.description,
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


class AbstractCharacterCard(AbstractCard, metaclass=abc.ABCMeta):
    """class AbstractCharacterCard."""

    def __init__(  # noqa: WPS211
        self,
        name: str,
        hp: int,
        ap: int,
        dp: int = 0,
        description: str = "",
    ) -> None:
        """
        Constructor for AbstractCharacterCard.

        :param name: Name of the card.
        :param hp: Health points of the card.
        :param ap: Attack points of the card.
        :param dp: Defense points of the card.
        :param description: Description of the card.
        :raises ValueError: If the hp, ap or dp is negative.
        """
        super().__init__(
            name=name,
            description=description,
        )
        self._hp: int = hp
        self._ap: int = ap
        self._dp: int = dp
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

    def is_alive(self) -> bool:
        """
        Check if the card is alive.

        :return: True if the card is alive, False otherwise.
        """
        return self.hp > 0

    def attack_card(self, card: "AbstractCharacterCard") -> None:
        """
        Attack a card.

        :param card: The card to attack.
        """
        card._receive_damage(self.ap)  # noqa: WPS437

    def _receive_damage(self, damage: int) -> None:
        """
        Receive damage.

        :param damage: The damage to receive.
        """
        if damage > self.dp:
            self._hp -= damage - self.dp


class PlayableCard(object):
    """class PlayableCard."""

    def __init__(self, cost: int):
        """
        Constructor for PlayableCard.

        :param cost: The cost of the card.
        """
        self._cost = cost

    @property
    def cost(self) -> int:
        """
        Getter for cost.

        :return: cost.
        """
        return self._cost
