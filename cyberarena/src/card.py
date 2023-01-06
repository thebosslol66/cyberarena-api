from typing import Any, Dict

from cyberarena.src.card_base import CardAbstract


class Card(CardAbstract):
    """Card class."""

    @classmethod
    def create_card_from_json(cls, json: Dict[str, Any]) -> CardAbstract:
        """
        Create a card from a json.

        :param json: The json to create the card from.
        :return: The card created.
        """
        name = json.get("name", "Cyber-Heisenberg")
        cost = json.get("cost", 1)
        hp = json.get("hp", 1)
        ap = json.get("ap", 0)
        return Card(name, cost, hp, ap)
