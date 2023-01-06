from cyberarena.src.card_base import CardAbstract


class Card(CardAbstract):
    """Card class."""

    def __init__(self, name: str, cost: int, hp: int, ap: int) -> None:
        """
        Constructor.

        :param name: Name of the card.
        :param cost: Cost of the card.
        :param hp: Hp of the card.
        :param ap: Ap of the card.
        """
        super().__init__(name, cost, hp, ap)

    def attack_card(self, card: CardAbstract) -> None:
        """
        Attack a card.

        :param card: Card to attack.
        """
        super().attack_card(card)

    def _receive_damage(self, damage: int) -> None:
        """
        Receive damage.

        :param damage: Damage to receive.
        """
        super()._receive_damage(damage)
        if super().is_alive():
            print("Card is alive")
        else:
            print("Card is dead")

    def __str__(self) -> str:
        """
        Convert to string.

        :return: String representation of the card.
        """
        return super().__str__()
