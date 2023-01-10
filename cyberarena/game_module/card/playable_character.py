from cyberarena.game_module.card.base import AbstractCharacterCard, PlayableCard


class PlayableCharacterCard(AbstractCharacterCard, PlayableCard):
    """Card class."""

    def __init__(  # noqa: WPS211
        self,
        name: str,
        cost: int,
        hp: int,
        ap: int,
        dp: int = 0,
        description: str = "",
    ) -> None:
        """
        Constructor for Card.

        :param name: Name of the card.
        :param cost: Cost of the card.
        :param hp: Health points of the card.
        :param ap: Attack points of the card.  # noqa: DAR003
        :param dp: Defense points of the card.
        :param description: Description of the card.
        :raise ValueError: If the cost, hp, ap or dp is negative.

        """
        super().__init__(  # noqa: WPS609
            name=name,
            description=description,
            hp=hp,
            ap=ap,
            dp=dp,
        )
        PlayableCard.__init__(self, cost)  # noqa: WPS609

    def __str__(self) -> str:
        """
        Return a string representation of the card.

        :return: A string representation of the card.
        """
        return "{0} ({1}/{2}/{3}) cost={4}".format(
            self.name,
            self.hp,
            self.ap,
            self.dp,
            self.cost,
        )

    def __repr__(self) -> str:
        """
        Return a string representation of the card.

        :return: A string representation of the card.
        """
        return "{0}, cost={1})".format(
            super().__repr__()[:-1],
            self.cost,
        )
