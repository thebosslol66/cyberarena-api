from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Boolean, Integer, String

from cyberarena.db.base import Base


class UserModel(Base):
    """Model for demo purpose."""

    __tablename__ = "user_model"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    username = Column(
        String(length=200),  # noqa: WPS432
        unique=True,
        nullable=False,
    )
    password = Column(String(length=200), nullable=False)  # noqa: WPS432
    email = Column(
        String(length=200),  # noqa: WPS432
        unique=True,
        nullable=False,
    )
    is_active = Column(Boolean(False))  # noqa: WPS432
    is_superuser = Column(Boolean(False))  # noqa: WPS432
