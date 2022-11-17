import bcrypt
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Boolean, Integer, String

from cyberarena.db.base import Base


class UserModel(Base):
    """Model to store Users."""

    __tablename__ = "user_model"

    id = Column(Integer(), primary_key=True, autoincrement=True)
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
    is_active = Column(Boolean(), nullable=False, default=False)  # noqa: WPS432
    is_superuser = Column(Boolean(), nullable=False, default=False)  # noqa: WPS432

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
