import abc
from typing import Any

from .base import AbstractCharacterCard


class AbstractDecorator(AbstractCharacterCard, metaclass=abc.ABCMeta):
    """class AbstractDecorator."""

    @abc.abstractmethod
    def __init__(self, card: AbstractCharacterCard) -> None:
        """
        Constructor for AbstractDecorator.

        :param card: Card to decorate.
        """
        self._card: AbstractCharacterCard = card

    def __repr__(self) -> str:
        """
        Return a string representation of the card.

        :return: A string representation of the card.
        """
        return self._card.__repr__()  # noqa: WPS609

    @property
    def name(self) -> str:
        """
        Getter for name.

        :return: name.
        """
        return self._card.name

    @property
    def description(self) -> str:
        """
        Getter for description.

        :return: description.
        """
        return self._card.description

    @property
    def hp(self) -> int:
        """
        Getter for hp.

        :return: hp.
        """
        return self._card.hp

    @property
    def ap(self) -> int:
        """
        Getter for ap.

        :return: ap.
        """
        return self._card.ap

    @property
    def dp(self) -> int:
        """
        Getter for dp.

        :return: dp.
        """
        return self._card.dp

    @property
    def cost(self) -> int:
        """
        Getter for cost.

        :return: cost.
        """
        return self._card.cost

    @property
    def card(self) -> AbstractCharacterCard:
        """
        Getter for card.

        :return: card.
        """
        return self._card

    def is_alive(self) -> bool:
        """
        Check if the card is alive.

        :return: True if the card is alive, False otherwise.
        """
        return self._card.is_alive()

    def attack_card(self, card: AbstractCharacterCard) -> None:
        """
        Attack a card.

        :param card: The card to attack.
        """
        self._card.attack_card(card)

    @abc.abstractmethod
    def refresh_card_reference(self) -> AbstractCharacterCard:
        """
        Return self or self._card if the decorator is useless or use.

        This function must be called after each action and after a turn

        :return: self or self._card.
        """
        return self

    def end_turn(self) -> None:
        """End the turn."""
        self._card.end_turn()

    def _receive_damage(self, damage: int) -> None:
        """
        Receive damage.

        :param damage: The damage to receive.
        """
        self._card._receive_damage(damage)

    def _add_attack_points_modifier(self, modifier: int) -> None:
        """
        Add attack points modifier.

        :param modifier: The modifier to add.
        """
        self._card._add_attack_points_modifier(modifier)


class _AbstractTurnDecorator(AbstractDecorator):
    """class AbstractTurnDecorator."""

    @abc.abstractmethod
    def __init__(
        self,
        card: AbstractCharacterCard,
        turns: int = 0,
        **kwargs: Any,
    ) -> None:
        """
        Constructor for AbstractTurnDecorator.

        :param card: Card to decorate.
        :param turns: Number of turns.
        :param kwargs: Keyword arguments.
        """
        super().__init__(card, **kwargs)
        self._turns: int = turns

    @abc.abstractmethod
    def end_turn(self) -> None:
        """End the turn."""
        self._turns -= 1

    @abc.abstractmethod
    def refresh_card_reference(self) -> AbstractCharacterCard:
        """
        Return self or self._card if the decorator is useless or use.

        This function must be called after each action and after a turn
        """


class DecoratorHealthBoost(AbstractDecorator):
    """class DecoratorHealthBoost."""

    def __init__(self, card: AbstractCharacterCard, hp_boost: int) -> None:
        """
        Constructor for DecoratorHealthBoost.

        :param card: Card to decorate.
        :param hp_boost: Health boost.
        """
        super().__init__(card)
        self._hp: int = hp_boost

    @property
    def hp(self) -> int:
        """
        Getter for hp.

        :return: hp.
        """
        return self.card.hp + self._hp

    def refresh_card_reference(self) -> AbstractCharacterCard:
        """
        Return self or self._card if the boost have 0 hp.

        This function must be called after each action and after a turn

        :return: self or self._card.
        """
        return self if self._hp > 0 else self.card

    def _receive_damage(self, damage: int) -> None:
        """
        Receive damage.

        :param damage: The damage to receive.
        """
        self._hp -= damage
        if self._hp < 0:
            self.card._receive_damage(-self._hp)
            self._hp = 0


class DecoratorDefenseBoost(AbstractDecorator):
    """class DecoratorDefenseBoost."""

    def __init__(self, card: AbstractCharacterCard, dp_boost: int) -> None:
        """
        Constructor for DecoratorDefenseBoost.

        :param card: Card to decorate.
        :param dp_boost: Defense boost.
        """
        super().__init__(card)
        self._dp: int = dp_boost

    @property
    def dp(self) -> int:
        """
        Getter for dp.

        :return: dp.
        """
        return self._dp + self.card.dp

    def refresh_card_reference(self) -> AbstractCharacterCard:
        """
        Return self or self._card if the boost have 0 hp.

        This function must be called after each action and after a turn

        :return: self or self._card.
        """
        return self if self._dp > 0 else self.card

    def _receive_damage(self, damage: int) -> None:
        """
        Receive damage.

        :param damage: The damage to receive.
        """
        if self._dp < damage:
            self.card._receive_damage(damage - self._dp)


class DecoratorTemporaryHitDefenseBoost(DecoratorDefenseBoost):
    """
    class DecoratorDefenseBoost.

    This class add shield to card but lose defense points for each hit it takes
    """

    def _receive_damage(self, damage: int) -> None:
        """
        Receive damage.

        :param damage: The damage to receive.
        """
        new_damage = max(0, damage - self._dp)
        self._dp -= damage
        if self._dp < 0:
            self._dp = 0
        self.card._receive_damage(new_damage)


class DecoratorTemporaryTurnDefenseBoost(_AbstractTurnDecorator, DecoratorDefenseBoost):
    """
    class DecoratorDefenseBoost.

    This class add shield to card but lose defense points
        at the end of the number of turn
    """

    def __init__(self, card: AbstractCharacterCard, dp_boost: int, turns: int) -> None:
        """
        Constructor for DecoratorDefenseBoost.

        :param card: Card to decorate.
        :param dp_boost: Defense boost.
        :param turns: Number of turn before losing the bonus
        """
        super().__init__(card=card, turns=turns, dp_boost=dp_boost)

    def end_turn(self) -> None:
        """End the turn."""
        super().end_turn()
        if self._turns == 0:
            self._dp = 0

    def refresh_card_reference(self) -> AbstractCharacterCard:
        """
        Return self or self._card if the boost have 0 hp.

        This function must be called after each action and after a turn

        :return: self or self._card.
        """
        return DecoratorDefenseBoost.refresh_card_reference(self)


class DecoratorTemporaryTurnAttackBoost(_AbstractTurnDecorator):
    """class DecoratorTemporaryTurnAttackBoost.

    This class add attack points to card but losethe bonus
        at the end of the number of turn
    """

    def __init__(self, card: AbstractCharacterCard, ap_boost: int, turns: int) -> None:
        """
        Constructor for DecoratorTemporaryTurnAttackBoost.

        :param card: Card to decorate.
        :param ap_boost: Attack boost.
        :param turns: Number of turn before losing the bonus
        """
        super().__init__(card=card, turns=turns)
        self._ap: int = ap_boost

    @property
    def ap(self) -> int:
        """
        Getter for ap.

        :return: ap.
        """
        return self._ap + self.card.ap

    def end_turn(self) -> None:
        """End the turn."""
        super().end_turn()
        if self._turns <= 0:
            self._ap = 0

    def refresh_card_reference(self) -> AbstractCharacterCard:
        """
        Return self or self._card if the boost have 0 hp.

        This function must be called after each action and after a turn

        :return: self or self._card.
        """
        return self if self._ap > 0 else self.card

    def attack_card(self, card: AbstractCharacterCard) -> None:
        """
        Attack a card.

        :param card: The card to attack.
        """
        self.card._add_attack_points_modifier(self._ap)
        self.card.attack_card(card)
