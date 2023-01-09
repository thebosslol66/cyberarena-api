from cyberarena.src.card_base import CardAbstract


class Card(CardAbstract):
    """Card class."""

    def __init__(  # noqa: WPS211
        self,
        name: str,
        cost: int,
        hp: int,
        ap: int,
        dp: int = 0,
    ) -> None:
        """
        Constructor for Card.

        :param name: Name of the card.
        :param cost: Cost of the card.
        :param hp: Health points of the card.
        :param ap: Attack points of the card.
        :param dp: Defense points of the card.
        :raises ValueError: If the cost, hp, ap or dp is negative.
        """
        super().__init__(name, hp, ap)
        self._cost: int = cost
        self._dp: int = dp
        if self._dp < 0 or self._cost < 0:
            raise ValueError("The dp or cost is negative.")

    @property
    def cost(self) -> int:
        """
        Getter for cost.

        :return: cost.
        """
        return self._cost

    @property
    def dp(self) -> int:
        """
        Getter for dp.

        :return: dp.
        """
        return self._dp

    def _receive_damage(self, damage: int) -> None:
        """
        Receive damage.

        :param damage: The damage to receive.
        """
        if damage > self._dp:
            self._hp -= damage - self._dp
