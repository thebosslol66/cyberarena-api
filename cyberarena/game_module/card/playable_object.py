import typing

from card import AbstractCard


class PlayableObjectCard(AbstractCard):
    """class PlayableObjectCard."""

    # TODO: Add logic of object card. It must use decorator methods

    def __str__(self) -> str:
        """
        Return a string representation of the card.

        :return: A string representation of the card.
        """
        return "Object card: {0}".format(super().__str__())

    def __repr__(self) -> str:
        """
        Return a string representation of the card.

        :return: A string representation of the card.
        """
        return repr(super())

    def to_dict(self) -> typing.Dict[str, str | int]:
        """
        Getter for json of the card.

        :raises NotImplementedError: Your darone is not implemented
        """
        raise NotImplementedError()
