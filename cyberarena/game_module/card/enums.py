import enum


class ObjectCardType(str, enum.Enum):  # noqa: WPS600
    """
    Enum for listing different type of cards.

    This instead of CardType enum, make difference between car objects, character cards
    and player card.
    """

    OBJECT = "object"
    CHARACTER = "character"
    PLAYER = "player"


class ObjectCardRace(str, enum.Enum):  # noqa: WPS600
    """Enum for listing different race of cards."""

    HUMAN = "human"
    ROBOT = "robot"
    ALIEN = "alien"
    MUTANT = "mutant"


class ObjectCardRarity(str, enum.Enum):  # noqa: WPS600
    """Enum for listing different rarity of cards."""

    COMMON = "common"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"
