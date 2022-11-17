from typing import List, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from cyberarena.db.dependencies import get_db_session
from cyberarena.db.models.user_model import UserModel


class UserDAO:
    """Class for accessing user table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_user(
        self,
        username: str,
        email: str,
        password: str,
    ) -> None:
        """
        Add single user to session.

        :param username: name of a user.
        :param email: email of a user.
        :param password: password of a user.
        """
        user = UserModel(username=username, email=email)
        user.set_password(password)
        self.session.add(
            user,
        )

    async def get_user_by_username(self, username: str) -> Optional[UserModel]:
        """
        Get specific user model.

        :param username: username of user instance.
        :return: user model.
        """
        query = select(UserModel).where(UserModel.username == username)
        rows = await self.session.execute(query)
        try:
            return rows.scalars().one()
        except Exception:
            return None

    async def get_user_by_email(self, email: str) -> Optional[UserModel]:
        """
        Get specific user model.

        :param email: email of user instance.
        :return: user model.
        """
        query = select(UserModel).where(UserModel.email == email)
        rows = await self.session.execute(query)
        try:
            return rows.scalars().one()
        except Exception:
            return None

    async def get_user_by_id(self, _id: int) -> Optional[UserModel]:
        """
        Get specific user model.

        :param _id: id of user instance.
        :return: user model.
        """
        query = select(UserModel).where(UserModel.id == _id)
        rows = await self.session.execute(query)
        try:
            return rows.scalars().one()
        except Exception:
            return None

    async def get_all_users(self, limit: int, offset: int) -> List[UserModel]:
        """
        Get all user models with limit/offset pagination.

        :param limit: limit of users.
        :param offset: offset of users.
        :return: stream of users.
        """
        raw_users = await self.session.execute(
            select(UserModel).limit(limit).offset(offset),
        )

        return raw_users.scalars().fetchall()

    async def filter(
        self,
        username: Optional[str] = None,
        email: Optional[str] = None,
        _id: Optional[int] = None,
    ) -> List[UserModel]:
        """
        Get specific user model.

        :param username: username of user instance.
        :param email: email of user instance.
        :param _id: id of user instance.
        :return: user models.
        """
        query = select(UserModel)
        if username:
            query = query.where(UserModel.username == username)
        if email:
            query = query.where(UserModel.email == email)
        if _id:
            query = query.where(UserModel.id == _id)
        rows = await self.session.execute(query)
        return rows.scalars().fetchall()

    async def update_superuser(self, _id: int, superuser: bool) -> None:
        """
        Update superuser status of user.

        :param _id: id of user instance.
        :param superuser: superuser status of user.
        """
        query = select(UserModel).where(UserModel.id == _id)
        rows = await self.session.execute(query)
        user = rows.scalars().one()
        user.superuser = superuser
        self.session.add(user)

    async def update_password(self, _id: int, password: str) -> None:
        """
        Update password of user.

        :param _id: id of user instance.
        :param password: password of user.
        """
        query = select(UserModel).where(UserModel.id == _id)
        rows = await self.session.execute(query)
        user = rows.scalars().one()
        user.password = password
        self.session.add(user)

    async def update_email(self, _id: int, email: str) -> None:
        """
        Update email of user.

        :param _id: id of user instance.
        :param email: email of user.
        """
        query = select(UserModel).where(UserModel.id == _id)
        rows = await self.session.execute(query)
        user = rows.scalars().one()
        user.email = email
        self.session.add(user)

    async def update_username(self, _id: int, username: str) -> None:
        """
        Update username of user.

        :param _id: id of user instance.
        :param username: username of ugit ser.
        """
        query = select(UserModel).where(UserModel.id == _id)
        rows = await self.session.execute(query)
        user = rows.scalars().one()
        user.username = username
        self.session.add(user)

    async def delete_user(self, _id: int) -> None:
        """
        Delete user.

        :param _id: id of user instance.
        """
        query = select(UserModel).where(UserModel.id == _id)
        rows = await self.session.execute(query)
        user = rows.scalars().one()
        await self.session.delete(user)

    async def update_active(self, _id: int, active: bool) -> None:
        """
        Update active status of user.

        :param _id: id of user instance.
        :param active: active status of user.
        """
        query = select(UserModel).where(UserModel.id == _id)
        rows = await self.session.execute(query)
        user = rows.scalars().one()
        user.active = active
        self.session.add(user)
