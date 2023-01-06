import random
from typing import List

from cyberarena.src.card import Card


class Deck(Card):
    """Deck Class."""

    def __init__(self) -> None:
        """Constructor."""
        self.__deck: List[Card] = []
        self.__deckSize = 20
        self.__init_deck()

    def __init_deck(self) -> None:
        """Initialize the deck."""
        for _ in range(0, self.__deckSize):
            self.__deck.append(Card("Cyber-Heisenberg", 1, 1, 1))

    def get_deck_size(self) -> int:
        """
        Get the deck size.

        :return: The deck size.
        """
        return self.__deckSize

    def get_random_card(self) -> Card:
        """
        Get a random card from the deck.

        :return: A random card.
        """
        return self.__deck[random.randint(0, self.__deckSize)]
