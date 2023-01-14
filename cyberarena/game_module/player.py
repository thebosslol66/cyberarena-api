from cyberarena.game_module.card.base import AbstractCard
from cyberarena.game_module.card.playable import Playable as PlayableCard
from cyberarena.game_module.deck import Deck
from cyberarena.game_module.hand import Hand


class Player:
    """Player Class."""

    def __init__(self, name: str) -> None:
        """
        Constructor.

        :param name: Name of the player.
        """
        self.name = name
        self.__deck = Deck()
        self.__hand = Hand(self.__deck)
        self.life = 20
        self.mana = 0
        self.mana_max = 10

    def get_mana(self) -> int:
        """
        Get the mana of the player.

        :return: The mana of the player.
        """
        return self.mana

    def draw_card(self) -> None:
        """Draw a card."""
        self.__hand.get_random_card()

    def use_card(self, card: PlayableCard) -> AbstractCard:
        """
        Use a card.

        :param card: Card to use.
        :return: the card used or a card with name "None".
        """
        if card.get_type() != "Playable":
            # todo: fairé réaction à attaque d'un champ
            pass

        res: PlayableCard = self.__hand.use_card(card, self.mana)
        if res.get_cost != 0:
            self.mana -= res.get_cost
            print("Card used")
            return res
        print("Card not used")
        return PlayableCard("None", 0, 0, 0, 0)

    def use_card_debug(self, index: int) -> AbstractCard:
        """
        Use a card debug mode.

        :param index: index of the card to get.
        :return: the card used or a card with name "None".
        """
        res: PlayableCard = self.__hand.use_card_debug(index, self.mana)
        if res.get_cost != 0:
            self.mana -= res.get_cost
            print("Card used")
            return res
        print("Card not used")
        return PlayableCard("None", 0, 0, 0, 0)

    def increase_mana(self, value: int) -> int:
        """
        Increase the mana of the player.

        :param value: Value to increase.
        :return: The new mana value.
        """
        self.mana += value
        if self.mana > self.mana_max:
            self.mana = self.mana_max
        return self.mana

    def debug_get_deck(self) -> Deck:
        """
        Get the deck of the player.

        :return: The deck of the player.
        """
        return self.__deck

    def debug_get_hand(self) -> Hand:
        """
        Get the hand of the player.

        :return: The hand of the player.
        """
        return self.__hand
