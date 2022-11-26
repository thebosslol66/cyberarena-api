from typing import Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from cyberarena.db.dependencies import get_db_session
from cyberarena.db.models.game_model import GameModel


class GameDAO:
    """Class for accessing game table"""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_game(self, player1: int, player2: int, terrain: str) -> None:
        """
        Add single game to session.

        :param player1: name of player 1.
        :param player2: name of player 2.
        :param terrain: name of terrain.
        :param winner: name of winner.
        """
        game = GameModel(player1=player1, player2=player2, terrain=terrain)
        self.session.add(game)

    async def get_game_by_id(self, id: int) -> Optional[GameModel]:
        """
        Get specific game model.

        :param id: id of game instance.
        :return: game model.
        """
        query = select(GameModel).where(GameModel.id == id)
        rows = await self.session.execute(query)
        try:
            return rows.scalars().one()
        except Exception:
            return None

    async def get_game_by_player(self, player: int) -> Optional[GameModel]:
        """
        Get specific game model.

        :param player: id of player instance.
        :return: game model.
        """
        query = select(GameModel).where(
            GameModel.player1 == player or GameModel.player2 == player,
        )
        rows = await self.session.execute(query)
        try:
            return rows.scalars().fetchall()
        except Exception:
            return None

    async def get_game_by_terrain(self, terrain: str) -> Optional[GameModel]:
        """
        Get specific game model.

        :param terrain: name of terrain instance.
        :return: game model.
        """
        query = select(GameModel).where(GameModel.terrain == terrain)
        rows = await self.session.execute(query)
        return rows.scalars().fetchall()

    async def get_game_by_winner(self, winner: int) -> Optional[GameModel]:
        """
        Get specific game model.

        :param winner: id of winner instance.
        :return: game model.
        """
        query = select(GameModel).where(GameModel.winner == winner)
        rows = await self.session.execute(query)
        return rows.scalars().fetchall()
