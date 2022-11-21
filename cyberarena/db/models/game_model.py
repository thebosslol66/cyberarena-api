from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer

from cyberarena.db.base import Base


class GameModel(Base):
    """Model to store Games."""

    __tablename__ = "game_model"

    id = Column(Integer, primary_key=True, index=True)
