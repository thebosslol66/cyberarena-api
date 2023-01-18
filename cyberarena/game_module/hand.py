from typing import List

from cyberarena.game_module.card import PlayableCharacterCard
from cyberarena.game_module.deck import Deck


class Hand:
    """Hand Class."""

    def __init__(self, deck: Deck) -> None:
        """
        Constructor.

        :param deck: Deck assigned to the Hand.
        """
        self.__hand: List[PlayableCharacterCard] = []
        self.__Deck = deck

    def __len__(self) -> int:
        """
        Get the hand size.

        :return: The hand size.
        """
        return len(self.__hand)

    def get_random_card(self) -> PlayableCharacterCard:
        """
        Get a random card from the deck.

        :return: A random card from the deck.
        """
        card = self.__Deck.get_random_card()
        if card.name == "None":
            pass
        if card:
            self.__hand.append(card)
        return card

    def use_card(self, card: PlayableCharacterCard, mana: int) -> PlayableCharacterCard:
        """
        Use a card.

        :param card: Card to use.
        :param mana: mana of the player.
        :return: True if the card is used, False otherwise.
        """
        if card.cost <= mana:
            self.__hand.remove(card)
            return card
        return PlayableCharacterCard("None", 0, 0, 0, 0)

    def use_card_debug(self, index: int, mana: int) -> PlayableCharacterCard:
        """
        Use a card.

        :param index: index of the card tu get.
        :param mana: mana of the player.
        :return: True if the card is used, False otherwise.
        """
        card = self.__hand[index]
        if self.__hand[index].cost <= mana:
            self.__hand.remove(self.__hand[index])
            return card
        return PlayableCharacterCard("None", 0, 0, 0, 0)

    def get_hand(self) -> List[PlayableCharacterCard]:
        """
        Get the hand.

        :return: The hand.
        """
        return self.__hand

    def cheat_add_card(self, card: PlayableCharacterCard) -> None:
        """
        Add a card to the hand.

        :param card: Card to add.
        """
        self.__hand.append(card)
