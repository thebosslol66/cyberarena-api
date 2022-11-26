from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String

from cyberarena.db.base import Base


class GameModel(Base):
    """Model to store Games."""

    __tablename__ = "game_model"

    id = Column(Integer(), primary_key=True, autoincrement=True)

    player1 = Column(String(length=200), nullable=False)  # noqa: WPS432

    player2 = Column(String(length=200), nullable=False)  # noqa: WPS432

    terrain = Column(String(length=200), nullable=False)  # noqa: WPS432

    winner = Column(String(length=200), nullable=True)  # noqa: WPS432
