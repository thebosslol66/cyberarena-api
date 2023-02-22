import typing

from .base import AbstractCharacterCard
from .enums import ObjectCardRace, ObjectCardRarity


class PlayableCharacterCard(AbstractCharacterCard):
    """Card class."""

    def __init__(  # noqa: WPS211
        self,
        name: str,
        cost: int,
        hp: int,
        ap: int,
        dp: int = 0,
        description: str = "",
        rarity: ObjectCardRarity = ObjectCardRarity.COMMON,
        race: ObjectCardRace = ObjectCardRace.HUMAN,
    ) -> None:
        """
        Constructor for Card.

        :param name: Name of the card.
        :param cost: Cost of the card.
        :param hp: Health points of the card.
        :param ap: Attack points of the card.  # noqa: DAR003
        :param dp: Defense points of the card.
        :param description: Description of the card.
        :param rarity: Rarity of the card.
        :param race: Race of the card.
        :raise ValueError: If the cost, hp, ap or dp is negative.

        """
        super().__init__(  # noqa: WPS609
            name=name,
            description=description,
            hp=hp,
            ap=ap,
            dp=dp,
            cost=cost,
            rarity=rarity,
            race=race,
        )

    def __str__(self) -> str:
        """
        Return a string representation of the card.

        :return: A string representation of the card.
        """
        return "Character card: {0} ({1}/{2}/{3}) cost={4} rarity={5} race={6}".format(
            self.name,
            self.hp,
            self.ap,
            self.dp,
            self.cost,
            self.rarity,
            self.race,
        )

    def __repr__(self) -> str:
        """
        Return a string representation of the card.

        :return: A string representation of the card.
        """
        return "{0}, cost={1})".format(
            repr(super())[:-1],
            self.cost,
        )

    def to_dict(self) -> typing.Dict[str, typing.Union[str, int]]:
        """
        Return a dictionary representation of the card.

        :raises NotImplementedError: Your darone is not implemented
        """
        raise NotImplementedError()
