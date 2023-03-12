import json
import os
import random
from fnmatch import fnmatch
from typing import List, Optional

from loguru import logger

from .card import AbstractCard, PlayableCharacterCard
from .card.playable_character import from_dict
from .settings import settings


class Deck(object):
    """Deck Class."""

    def __init__(self) -> None:
        """Constructor."""
        self.__deck: List[AbstractCard] = []
        self.__deckSize = settings.deck_size
        self.__init_deck()

    def use_card(self, card: AbstractCard, mana: int, currid: int) -> AbstractCard:
        """
        Use a card.

        :param card: Card to use.
        :param mana: Mana of the player.
        :param currid: ID of the current card.
        :return: the card used or a card with name "None".
        """
        if card.cost <= mana:
            card.id = currid
            return card
        return PlayableCharacterCard("None", 0, 0, 0)

    def get_random_card(self) -> Optional[AbstractCard]:
        """
        Get a random card from the deck.

        :return: A random card.
        """
        if self.__deck:
            return self.__deck.pop()
        return None

    def __len__(self) -> int:
        """
        Get the size of the deck.

        :return: The size of the deck.
        """
        return len(self.__deck)

    def __init_deck(self) -> None:
        """Initialize the deck."""
        logger.error("Deck size: ", str(self.__deckSize))
        # Le chemin du répertoire contenant les fichiers json
        path = settings.card_path

        # Une liste vide pour stocker les données des fichiers json
        data_list = []

        # On parcourt tous les répertoires et sous-répertoires du chemin
        for dirpath, _dirnames, filenames in os.walk(path):
            # On parcourt tous les fichiers du répertoire courant
            for file in filenames:
                # On vérifie si le fichier se nomme data.json
                if fnmatch(file, "data.json"):
                    # On construit le chemin complet du fichier
                    file_path = os.path.join(dirpath, file)
                    # On ouvre le fichier en mode lecture
                    with open(file_path) as f:
                        # On charge le contenu du fichier comme un objet Python
                        data = json.load(f)
                        data = {k: v for k, v in data.items() if k != "card_type"}
                        data = {
                            k if k != "id" else "id_pic": v for k, v in data.items()
                        }

                        # On ajoute l'objet à la liste
                        data_list.append(data)

        # On affiche la liste des données récupérées
        logger.error(len(data_list))
        for i in range(0, 12):
            logger.error(type(data_list[i]))
            card = from_dict(data_list[i])
            self.__deck.append(card)
            self.__deck.append(card)
        random.shuffle(self.__deck)
