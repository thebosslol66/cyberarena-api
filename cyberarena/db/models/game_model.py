from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String

from cyberarena.db.base import Base

class GameModel(Base):
    """Model to store Games."""

    __tablename__ = "game_model"
    