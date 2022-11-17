# flake8: noqa

import uuid

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from cyberarena.db.dao.user_dao import UserDAO

######################################################################
#                       TESTS USER SIGNUP                            #
######################################################################


@pytest.mark.anyio
async def test_new_sign_up(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """
    Checks the register endpoint.

    :param client: client for the app.
    :param fastapi_app: current FastAPI application.
    """
    url = fastapi_app.url_path_for("sign_up")
    test_name = uuid.uuid4().hex
    password = "aAZ?o2aaaaa"
    email = "test@test.com"
    response = await client.post(
        url,
        json={
            "username": test_name,
            "password": password,
            "email": email,
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == 0

    dao = UserDAO(dbsession)
    instance1 = await dao.get_user_by_username(test_name)
    assert instance1 is not None
    assert instance1.username == test_name
    assert instance1.email == email
    assert instance1.is_correct_password(password)
    assert instance1.is_superuser is False
    assert instance1.is_active is False

    instance2 = await dao.get_user_by_email(email)
    assert instance1 == instance2


@pytest.mark.anyio
async def test_sign_up_username_too_short(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """
    Checks the register endpoint.

    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
    """
    url = fastapi_app.url_path_for("sign_up")
    test_name = "a"
    password = "aAZ?o2aaaaa"
    email = "test@test.com"
    response = await client.post(
        url,
        json={
            "username": test_name,
            "password": password,
            "email": email,
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == 1

    dao = UserDAO(dbsession)
    instance1 = await dao.get_user_by_username(test_name)
    assert instance1 is None


@pytest.mark.anyio
async def test_sign_up_with_space_in_username(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """
    Checks the register endpoint.

    :param client: client for the app.
    :param fastapi_app: current FastAPI application.
    """
    url = fastapi_app.url_path_for("sign_up")
    test_name = uuid.uuid4().hex + " " + uuid.uuid4().hex
    password = "aAZ?o2aaaaa"
    email = "test@test.com"
    response = await client.post(
        url,
        json={
            "username": test_name,
            "password": password,
            "email": email,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == 1

    dao = UserDAO(dbsession)
    instance1 = await dao.get_user_by_username(test_name)
    assert instance1 is None

    instance2 = await dao.get_user_by_email(email)
    assert instance2 is None


@pytest.mark.anyio
async def test_sign_up_with_special_caracters_username(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """
    Checks the register endpoint.

    :param client: client for the app.
    :param fastapi_app: current FastAPI application.
    """
    url = fastapi_app.url_path_for("sign_up")
    for special_caracter in "!@#$%^&*()_+{}|:<>?[]\\;',./`~":
        test_name = uuid.uuid4().hex + special_caracter
        password = "aAZ?o2aaaaa"
        email = "test@test.com"
        response = await client.post(
            url,
            json={
                "username": test_name,
                "password": password,
                "email": email,
            },
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["status"] == 1

        dao = UserDAO(dbsession)
        instance1 = await dao.get_user_by_username(test_name)
        assert instance1 is None

        instance2 = await dao.get_user_by_email(email)
        assert instance2 is None


@pytest.mark.anyio
async def test_sign_up_with_existing_username(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """
    Checks the register endpoint.

    :param client: client for the app.
    :param fastapi_app: current FastAPI application.
    """
    url = fastapi_app.url_path_for("sign_up")
    test_name = uuid.uuid4().hex
    password = "aAZ?o2aaaaa"
    email = "test@test.com"

    dao = UserDAO(dbsession)
    await dao.create_user(
        username=test_name,
        password=password,
        email=email,
    )

    response = await client.post(
        url,
        json={
            "username": test_name,
            "password": "1" + password,
            "email": "t" + email,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == 4

    instance1 = await dao.get_user_by_email("t" + email)
    assert instance1 is None


@pytest.mark.anyio
async def test_sign_up_with_invalid_email(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """
    :param fastapi_app: current FastAPI application.
    :param client: client for the app.
    :param dbsession: database session.
    """

    url = fastapi_app.url_path_for("sign_up")
    test_name = uuid.uuid4().hex
    password = "aAZ?o2aaaaa"
    emails = [
        "test@test",
        "test@test.",
        "test@test..com",
        "test/test.com",
        "test/test@test.com",
        "test@test@test.com",
        "test<@test.com",
    ]
    for email in emails:
        response = await client.post(
            url,
            json={
                "username": test_name,
                "password": password,
                "email": email,
            },
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["status"] == 3

        dao = UserDAO(dbsession)
        instance1 = await dao.get_user_by_email(email)
        assert instance1 is None

        instance2 = await dao.get_user_by_username(test_name)
        assert instance2 is None


@pytest.mark.anyio
async def test_sign_up_with_existing_email(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """
    Checks the register endpoint.

    :param client: client for the app.
    :param fastapi_app: current FastAPI application.
    """
    url = fastapi_app.url_path_for("sign_up")
    test_name = uuid.uuid4().hex
    password = "aAZ?o2aaaaa"
    email = "test@test.com"

    dao = UserDAO(dbsession)
    await dao.create_user(
        username=test_name,
        password=password,
        email=email,
    )

    response = await client.post(
        url,
        json={
            "username": "t" + test_name,
            "password": "1" + password,
            "email": email,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == 5


@pytest.mark.anyio
async def test_sign_up_two_user_with_same_password(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """
    Checks the register endpoint.

    :param client: client for the app.
    :param fastapi_app: current FastAPI application.
    """
    url = fastapi_app.url_path_for("sign_up")
    test_name = uuid.uuid4().hex
    password = "aAZ?o2aaaaa"
    email = "test@test.com"

    dao = UserDAO(dbsession)
    await dao.create_user(
        username=test_name,
        password=password,
        email=email,
    )

    test_name2 = uuid.uuid4().hex
    email2 = "test2@test.com"

    response = await client.post(
        url,
        json={
            "username": test_name2,
            "password": password,
            "email": email2,
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == 0

    instance1 = await dao.get_user_by_username(test_name2)
    instance2 = await dao.get_user_by_username(test_name)
    assert instance1 is not None
    assert instance2 is not None
    assert instance1 != instance2


@pytest.mark.anyio
async def test_sign_up_password_without_upper_letter(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """
    Checks the register endpoint.

    :param client: client for the app.
    :param fastapi_app: current FastAPI application.
    """
    url = fastapi_app.url_path_for("sign_up")
    test_name = uuid.uuid4().hex
    password = "a?o2aaaaa"
    email = "test@test.com"

    response = await client.post(
        url,
        json={
            "username": test_name,
            "password": password,
            "email": email,
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == 2

    dao = UserDAO(dbsession)
    instance1 = await dao.get_user_by_username(test_name)
    assert instance1 is None


@pytest.mark.anyio
async def test_sign_up_password_without_lower_letter(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """
    Checks the register endpoint.

    :param client: client for the app.
    :param fastapi_app: current FastAPI application.
    """
    url = fastapi_app.url_path_for("sign_up")
    test_name = uuid.uuid4().hex
    password = "A?O2AAAAA"
    email = "test@test.com"

    response = await client.post(
        url,
        json={
            "username": test_name,
            "password": password,
            "email": email,
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == 2

    dao = UserDAO(dbsession)
    instance1 = await dao.get_user_by_username(test_name)
    assert instance1 is None


@pytest.mark.anyio
async def test_sign_up_password_without_number(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """
    Checks the register endpoint.

    :param client: client for the app.
    :param fastapi_app: current FastAPI application.
    """
    url = fastapi_app.url_path_for("sign_up")
    test_name = uuid.uuid4().hex
    password = "aAZ?oaaaaa"
    email = "test@test.com"

    response = await client.post(
        url,
        json={
            "username": test_name,
            "password": password,
            "email": email,
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == 2

    dao = UserDAO(dbsession)
    instance1 = await dao.get_user_by_username(test_name)
    assert instance1 is None


@pytest.mark.anyio
async def test_sign_up_password_without_special_character(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """
    Checks the register endpoint.

    :param client: client for the app.
    :param fastapi_app: current FastAPI application.
    """
    url = fastapi_app.url_path_for("sign_up")
    test_name = uuid.uuid4().hex
    password = "aAZo2aaaaa"
    email = "test@test.com"

    response = await client.post(
        url,
        json={
            "username": test_name,
            "password": password,
            "email": email,
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == 2

    dao = UserDAO(dbsession)
    instance1 = await dao.get_user_by_username(test_name)
    assert instance1 is None


@pytest.mark.anyio
async def test_sign_up_password_too_short(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """
    Checks the register endpoint.

    :param client: client for the app.
    :param fastapi_app: current FastAPI application.
    """
    url = fastapi_app.url_path_for("sign_up")
    test_name = uuid.uuid4().hex
    password = "aAZ?o2a"
    email = "test@test.com"

    response = await client.post(
        url,
        json={
            "username": test_name,
            "password": password,
            "email": email,
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == 2

    dao = UserDAO(dbsession)
    instance1 = await dao.get_user_by_username(test_name)
    assert instance1 is None


######################################################################
#                        TEST USER SIGN IN                           #
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
async def test_sign_in(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """
    Checks the register endpoint.

    :param client: client for the app.
    :param fastapi_app: current FastAPI application.
    """
    url = fastapi_app.url_path_for("sign_in")
    username = ("test",)
    password = ("aAZ?o2aaaaa",)
    email = ("test@test.com",)

    await create_dummy_user(dbsession)

    response = await client.post(
        url,
        json={
            "username": username,
            "password": password,
        },
    )
