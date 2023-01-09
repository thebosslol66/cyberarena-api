import abc


class CardAbstract(metaclass=abc.ABCMeta):
    """class CardAbstract."""

    def __init__(self, name: str, hp: int, ap: int) -> None:
        """
        Constructor for CardAbstract.

        :param name: Name of the card.
        :param hp: Health points of the card.
        :param ap: Attack points of the card.
        :raises ValueError: If the hp or ap is negative.
        """
        self._name: str = name
        self._hp: int = hp
        self._ap: int = ap
        if self._hp < 0 or self._ap < 0:
            raise ValueError("The hp or ap is negative.")

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
        return self._name

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

        :return: The ap of this CardAbstract.
        """
        return self._ap

    def attack_card(self, card: "CardAbstract") -> None:
        """
        Attack a card.

        :param card: Card to attack.
        """
        CardAbstract._receive_damage(card, self.ap)  # noqa: WPS437

    def is_alive(self) -> bool:
        """
        Check if the card is alive.

        :return: True if the card is alive, False otherwise.
        """
        return self._hp > 0

    @abc.abstractmethod
    def _receive_damage(self, damage: int) -> None:
        """
        Receive damage.

        :param damage: Damage to receive.
        """
        self._hp -= damage
