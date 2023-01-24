from datetime import datetime, timedelta

import bcrypt
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import BigInteger, Boolean, DateTime, Integer, String

from cyberarena.db.base import Base


class UserModel(Base):
    """Model to store Users."""

    __tablename__ = "user_model"

    id = Column(Integer(), primary_key=True, autoincrement=True, nullable=False)
    username = Column(
        String(length=200),  # noqa: WPS432
        unique=True,
        nullable=False,
    )
    _password_hash = Column(String(length=128), nullable=False)  # noqa: WPS432
    email = Column(
        String(length=200),  # noqa: WPS432
        unique=True,
        nullable=False,
    )
    refresh_token_value = Column(String(length=128), nullable=True)  # noqa: WPS432
    is_active = Column(Boolean(), nullable=False, default=False)
    is_superuser = Column(Boolean(), nullable=False, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, default=datetime.utcnow)

    coins = Column(BigInteger(), nullable=False, default=0)
    last_daily_reward = Column(
        DateTime,
        default=lambda: datetime.utcnow() - timedelta(days=1),
        nullable=False,
    )

    @hybrid_property
    def password(self) -> str:
        """
        Password getter.

        :return: password.

        """
        return self._password_hash if self._password_hash else ""

    def set_password(self, plaintext: str) -> None:
        """

        Password setter.

        :param plaintext: password to set.

        """
        self._password_hash = bcrypt.hashpw(  # noqa: WPS601
            plaintext.encode("utf8"),
            bcrypt.gensalt(),
        ).decode("utf8")

    def is_correct_password(self, plaintext: str) -> bool:
        """
        Check if password is correct.

        :param plaintext: password to check
        :return: True if password is correct.
        """
        return bcrypt.checkpw(
            plaintext.encode("utf8"),
            self.password.encode("utf8"),
        )
