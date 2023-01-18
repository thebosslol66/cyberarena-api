import random
from typing import List

from cyberarena.game_module.card import PlayableCharacterCard
from cyberarena.game_module.settings import settings


class Deck(object):
    """Deck Class."""

    def __init__(self) -> None:
        """Constructor."""
        self.__deck: List[PlayableCharacterCard] = []
        self.__deckSize = settings.deck_size
        self.__init_deck()

    def use_card(self, card: PlayableCharacterCard, mana: int) -> PlayableCharacterCard:
        """
        Use a card.

        :param card: Card to use.
        :param mana: Mana of the player.
        :return: the card used or a card with name "None".
        """
        if card.cost <= mana:
            return card
        return PlayableCharacterCard("None", 0, 0, 0)

    def get_random_card(self) -> PlayableCharacterCard:
        """
        Get a random card from the deck.

        :return: A random card.
        """
        if self.__deck:
            print("pop")
            return self.__deck.pop()
        return PlayableCharacterCard("None", 0, 0, 0)

    def __len__(self) -> int:
        """
        Get the size of the deck.

        :return: The size of the deck.
        """
        return len(self.__deck)

    def __init_deck(self) -> None:
        """Initialize the deck."""
        for _ in range(0, self.__deckSize):

            self.__deck.append(PlayableCharacterCard("Cyber-Heisenberg", 1, 1, 1))
        random.shuffle(self.__deck)
