# flake8: noqa
import uuid
from datetime import datetime, timedelta
from typing import Callable

from _pytest.monkeypatch import MonkeyPatch
from fastapi import Depends, FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from cyberarena.db.dao.user_dao import UserDAO
from cyberarena.db.models.user_model import UserModel
from cyberarena.settings import settings
from cyberarena.web.api.connection.utils import get_current_user
from cyberarena.web.api.economy import utils


async def create_dummy_user(
    dbsession: AsyncSession,
    username: str = "test",
    password: str = "aAZ?o2aaaaa",
    email: str = "test@test.com",
) -> None:
    """
    Create a dummy user.

    :param dbsession: database session.
    :param username: username.
    :param password: password.
    :param email: email
    """
    dao = UserDAO(dbsession)
    await dao.create_user(
        username=username,
        password=password,
        email=email,
    )


def override_get_current_user(username: str) -> Callable[[], UserModel]:
    """
    Override get_current_user.

    :param username: username.
    :param user_dao: user dao.
    """

    async def func(
        user_dao: UserDAO = Depends(),
    ) -> UserModel:
        """
        Get current user.

        :param user_dao: user dao.
        :return: current user.
        """
        return await user_dao.get_user_by_username(username)

    return func


######################################################################
#                       TESTS DAILY REWARDS                          #
######################################################################


async def test_daily_rewards_login_after_signup(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """
    Tests that daily rewards works after signup.

    :param fastapi_app: current application.
    :param client: clien for the app.
    """
    url = fastapi_app.url_path_for("sign_up")
    username = uuid.uuid4().hex
    password = "aAZ?o2aaaaa"
    response = await client.post(
        url,
        json={
            "username": username,
            "password": password,
            "email": "test@test.com",
        },
    )
    assert response.status_code == status.HTTP_200_OK

    fastapi_app.dependency_overrides[get_current_user] = override_get_current_user(
        username,
    )

    url = fastapi_app.url_path_for("ask_daily_free_coins")
    response = await client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == settings.daily_coin_reward

    user_dao = UserDAO(dbsession)
    user = await user_dao.get_user_by_username(username)
    assert user.last_daily_reward.date() == utils.now().date()
    assert user.coins == settings.daily_coin_reward


async def test_daily_rewards_two_times_a_day(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """
    Tests that daily rewards isn't given twice a day.

    :param fastapi_app: current application.
    :param client: client for the app.
    """

    username = "test"
    await create_dummy_user(dbsession)
    dao = UserDAO(dbsession)

    fastapi_app.dependency_overrides[get_current_user] = override_get_current_user(
        username,
    )

    url = fastapi_app.url_path_for("ask_daily_free_coins")
    response = await client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == settings.daily_coin_reward

    url = fastapi_app.url_path_for("ask_daily_free_coins")
    response = await client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == 0
    assert (
        await dao.get_user_by_username(username)
    ).coins == settings.daily_coin_reward


async def test_daily_rewards_after_24_hours(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
    monkeypatch: MonkeyPatch,
) -> None:
    """
    Tests that daily rewards works for 2 consecutive days.

    :param fastapi_app: current application.
    :param client: client for the app.
    """
    username = "test"
    await create_dummy_user(dbsession)
    dao = UserDAO(dbsession)

    fastapi_app.dependency_overrides[get_current_user] = override_get_current_user(
        username,
    )

    url = fastapi_app.url_path_for("ask_daily_free_coins")
    response = await client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == settings.daily_coin_reward

    monkeypatch.setattr(utils, "now", lambda: datetime.now() + timedelta(days=1))

    url = fastapi_app.url_path_for("ask_daily_free_coins")
    response = await client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == settings.daily_coin_reward
    assert (
        await dao.get_user_by_username(username)
    ).coins == 2 * settings.daily_coin_reward
