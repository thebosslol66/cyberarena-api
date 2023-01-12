from enum import auto

from strenum import StrEnum


class ObjectCardType(StrEnum):
    """
    Enum for listing different type of cards.

    This instead of CardType enum, make difference between car objects, character cards
    and player card.
    """

    OBJECT = auto()
    CHARACTER = auto()
    PLAYER = auto()
