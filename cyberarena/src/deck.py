import random
from typing import List, Optional

from cyberarena.src.card import Card
from cyberarena.src.settings import settings


class Deck(Card):
    """Deck Class."""

    def __init__(self) -> None:
        """Constructor."""
        self.__deck: List[Card] = []
        self.__deckSize = settings.deck_size
        self.__init_deck()

    def __init_deck(self) -> None:
        """Initialize the deck."""
        for _ in range(0, self.__deckSize):
            self.__deck.append(Card("Cyber-Heisenberg", 1, 1, 1))
        random.shuffle(self.__deck)

    def get_random_card(self) -> Optional[Card]:
        """
        Get a random card from the deck.

        :return: A random card.
        """
        if len(self.__deck) > 0:
            return self.__deck.pop()
        else:
            return None

    def get_size(self) -> int:
        """
        Get the size of the deck.

        :return: The size of the deck.
        """
        return self.__deckSize
