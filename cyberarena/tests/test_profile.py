# flake8: noqa

import pytest
from _pytest.monkeypatch import MonkeyPatch
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from cyberarena.db.dao.user_dao import UserDAO
from cyberarena.web.api.connection import utils

######################################################################
#                     TESTS CHANGE PASSWORD                          #
######################################################################


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


@pytest.mark.anyio
async def test_change_password(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
    monkeypatch: MonkeyPatch,
) -> None:
    """Tests change password."""

    username = "test"
    password = "aAZ?o2aaaaa"
    new_password = "aAZ?o2aaaaa"

    await create_dummy_user(dbsession)

    monkeypatch.setattr(
        utils,
        "get_current_user",
        lambda: dao.get_user_by_username(username),
    )

    url = fastapi_app.url_path_for("change_password")
    response = await client.put(
        url,
        json={
            "old_password": password,
            "new_password": new_password,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    dao = UserDAO(dbsession)
    user = await dao.get_user_by_username(username)
    assert user.password != password
    assert user.password == new_password


@pytest.mark.anyio
async def test_change_password_protected_route(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    username = "test"
    password = "aAZ?o2aaaaa"
    new_password = "aAZ?o2aaaaa"

    await create_dummy_user(dbsession)

    url = fastapi_app.url_path_for("change_password")
    response = await client.put(
        url,
        json={
            "old_password": password,
            "new_password": new_password,
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    dao = UserDAO(dbsession)
    user = await dao.get_user_by_username(username)
    assert user.password == password


@pytest.mark.anyio
async def test_change_password_wrong_old_password(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
    monkeypatch: MonkeyPatch,
) -> None:
    """Tests change password with wrong old password."""

    username = "test"
    password = "aAZ?o2aaaaa"
    new_password = "aAZ?o2aaaaa"
    wrong_password = "aAZ?o2aaaaa"

    await create_dummy_user(dbsession)

    monkeypatch.setattr(
        utils,
        "get_current_user",
        lambda: dao.get_user_by_username(username),
    )

    url = fastapi_app.url_path_for("change_password")
    response = await client.put(
        url,
        json={
            "old_password": wrong_password,
            "new_password": new_password,
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    dao = UserDAO(dbsession)
    user = await dao.get_user_by_username(username)
    assert user.password == password


@pytest.mark.anyio
async def test_change_password_same_password(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
    monkeypatch: MonkeyPatch,
) -> None:
    """Test change password with same password"""
    username = "test"
    password = "aAZ?o2aaaaa"

    await create_dummy_user(dbsession)

    monkeypatch.setattr(
        utils,
        "get_current_user",
        lambda: dao.get_user_by_username(username),
    )

    url = fastapi_app.url_path_for("change_password")
    response = await client.put(
        url,
        json={
            "old_password": password,
            "new_password": password,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    dao = UserDAO(dbsession)
    user = await dao.get_user_by_username(username)
    assert user.password == password


@pytest.mark.anyio
async def test_change_password_wrong_new_password(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
    monkeypatch: MonkeyPatch,
) -> None:
    """Tests change password with wrong new password."""

    username = "test"
    password = "aAZ?o2aaaaa"
    new_passwords = ["a?o2aaaaa", "A?O2AAAAA", "aAZ?oaaaaa", "aAZo2aaaaa", "aAZ?o2a"]

    await create_dummy_user(dbsession)

    monkeypatch.setattr(
        utils,
        "get_current_user",
        lambda: dao.get_user_by_username(username),
    )

    url = fastapi_app.url_path_for("change_password")
    for new_password in new_passwords:
        response = await client.put(
            url,
            json={
                "old_password": password,
                "new_password": new_password,
            },
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        dao = UserDAO(dbsession)
        user = await dao.get_user_by_username(username)
        assert user.password == password


######################################################################
#                      TESTS CHANGE EMAIL                            #
######################################################################


@pytest.mark.anyio
async def test_change_email(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
    monkeypatch: MonkeyPatch,
) -> None:
    """Tests change email."""

    username = "test"
    password = "aAZ?o2aaaaa"
    new_email = "test2@test.com"
    old_email = "test@test.com"

    await create_dummy_user(dbsession)

    monkeypatch.setattr(
        utils,
        "get_current_user",
        lambda: dao.get_user_by_username(username),
    )

    url = fastapi_app.url_path_for("change_email")
    response = await client.put(
        url,
        json={
            "password": password,
            "new_email": new_email,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    dao = UserDAO(dbsession)
    user = await dao.get_user_by_username(username)
    assert user.email != old_email
    assert user.email == new_email
    assert user.is_active is False


@pytest.mark.anyio
async def test_change_email_protected_route(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """Tests change email without be logged."""

    username = "test"
    password = "aAZ?o2aaaaa"
    new_email = "test2@test.com"
    old_email = "test@test.com"

    await create_dummy_user(dbsession)

    url = fastapi_app.url_path_for("change_email")
    response = await client.put(
        url,
        json={
            "password": password,
            "new_email": new_email,
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    dao = UserDAO(dbsession)
    user = await dao.get_user_by_username(username)
    assert user.email == old_email


@pytest.mark.anyio
async def test_change_email_wrong_password(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
    monkeypatch: MonkeyPatch,
) -> None:
    """Tests change email with wrong password."""

    username = "test"
    password = "aAZ?o2aaaaa"
    wrong_password = "aAZ?o2aaaaaa"
    old_email = "test@test.com"
    new_email = "test2@test.com"

    await create_dummy_user(dbsession)

    monkeypatch.setattr(
        utils,
        "get_current_user",
        lambda: dao.get_user_by_username(username),
    )

    url = fastapi_app.url_path_for("change_email")
    response = await client.put(
        url,
        json={
            "password": password,
            "new_email": new_email,
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    dao = UserDAO(dbsession)
    user = await dao.get_user_by_username(username)
    assert user.email != new_email
    assert user.email == old_email


@pytest.mark.anyio
async def test_change_email_same_email(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
    monkeypatch: MonkeyPatch,
) -> None:
    """Tests change email with same email."""
    username = "test"
    password = "aAZ?o2aaaaa"
    old_email = "test@test.com"

    await create_dummy_user(dbsession)

    monkeypatch.setattr(
        utils,
        "get_current_user",
        lambda: dao.get_user_by_username(username),
    )

    url = fastapi_app.url_path_for("change_email")
    response = await client.put(
        url,
        json={
            "password": password,
            "new_email": old_email,
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    dao = UserDAO(dbsession)
    user = await dao.get_user_by_username(username)
    assert user.email == old_email


@pytest.mark.anyio
async def test_change_email_wrong_email(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
    monkeypatch: MonkeyPatch,
) -> None:
    """Tests change email with wrong email."""
    username = "test"
    password = "aAZ?o2aaaaa"
    wrong_emails = [
        "test@test",
        "test@test.",
        "@test.com",
        "test.com",
        "test@testcom",
        "",
    ]

    await create_dummy_user(dbsession)

    monkeypatch.setattr(
        utils,
        "get_current_user",
        lambda: dao.get_user_by_username(username),
    )

    url = fastapi_app.url_path_for("change_email")
    for wrong_email in wrong_emails:
        response = await client.put(
            url,
            json={
                "password": password,
                "new_email": wrong_email,
            },
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        dao = UserDAO(dbsession)
        user = await dao.get_user_by_username(username)
        assert user.email != wrong_email


@pytest.mark.anyio
async def test_change_email_other_account_have_same_email(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
    monkeypatch: MonkeyPatch,
) -> None:
    """Tests change email with other account have same email."""
    username = "test"
    password = "aAZ?o2aaaaa"
    new_email = "test2@test.com"

    await create_dummy_user(dbsession)
    await create_dummy_user(dbsession, username="test2", email=new_email)

    monkeypatch.setattr(
        utils,
        "get_current_user",
        lambda: dao.get_user_by_username(username),
    )

    url = fastapi_app.url_path_for("change_email")
    response = await client.put(
        url,
        json={
            "password": password,
            "new_email": new_email,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    dao = UserDAO(dbsession)
    user = await dao.get_user_by_username(username)
    assert user.email != new_email


######################################################################
#                      TESTS CHANGE PASSWORD                         #
######################################################################
