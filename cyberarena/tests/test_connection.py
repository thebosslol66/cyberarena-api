# flake8: noqa
import datetime
import uuid

import pytest
from _pytest.monkeypatch import MonkeyPatch
from fastapi import FastAPI
from httpx import AsyncClient
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from cyberarena.db.dao.user_dao import UserDAO
from cyberarena.db.models.user_model import UserModel
from cyberarena.settings import settings
from cyberarena.web.api.connection import utils

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
    assert instance1.refresh_token_value is None
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
async def test_sign_in_username_correct(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """
    Checks the register endpoint.

    :param client: client for the app.
    :param fastapi_app: current FastAPI application.
    """
    url = fastapi_app.url_path_for("login_for_access_token")
    username = "test"
    password = "aAZ?o2aaaaa"
    email = "test@test.com"

    await create_dummy_user(dbsession)
    user_dao = UserDAO(dbsession)
    user = await user_dao.get_user_by_username(username)
    if user is None:
        raise ValueError("User is None")
    await user_dao.update_active(-1 if user.id is None else user.id, True)

    response = await client.post(
        url,
        data={
            "username": username,
            "password": password,
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )

    assert response.status_code == status.HTTP_200_OK
    at = response.json()["access_token"]
    assert at != ""
    rt = response.json()["refresh_token"]
    assert rt != ""
    assert response.json()["token_type"] == "Bearer"
    decoded_access_token = jwt.decode(
        at,
        settings.secret_key,
        algorithms=[settings.algorithm],
    )
    decoded_refresh_token = jwt.decode(
        rt,
        settings.secret_key,
        algorithms=[settings.algorithm],
    )
    user_from_db: UserModel = await user_dao.get_user_by_username(username)
    assert decoded_access_token["sub"] == str(
        user_from_db.id,
    )
    assert (
        decoded_access_token["exp"] - decoded_access_token["iat"]
        == settings.access_token_expire_minutes * 60
    )
    # TODO: check scopes

    user_from_db: UserModel = await user_dao.get_user_by_username(username)
    assert decoded_refresh_token["sub"] == str(
        user_from_db.id,
    )
    assert (
        decoded_refresh_token["exp"] - decoded_refresh_token["iat"]
        == settings.refresh_token_expire_minutes * 60
    )
    assert decoded_refresh_token["val"] == user.refresh_token_value


@pytest.mark.anyio
async def test_sign_in_email_correct(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """
    Checks the register endpoint.

    :param client: client for the app.
    :param fastapi_app: current FastAPI application.
    """
    url = fastapi_app.url_path_for("login_for_access_token")
    username = "test"
    password = "aAZ?o2aaaaa"
    email = "test@test.com"

    await create_dummy_user(dbsession)
    user_dao = UserDAO(dbsession)
    user = await user_dao.get_user_by_username(username)
    if user is None:
        raise ValueError("User is None")
    await user_dao.update_active(-1 if user.id is None else user.id, True)

    response = await client.post(
        url,
        data={
            "username": email,
            "password": password,
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )

    assert response.status_code == status.HTTP_200_OK
    at = response.json()["access_token"]
    assert at != ""
    rt = response.json()["refresh_token"]
    assert rt != ""
    assert response.json()["token_type"] == "Bearer"
    decoded_access_token = jwt.decode(
        at,
        settings.secret_key,
        algorithms=[settings.algorithm],
    )
    decoded_refresh_token = jwt.decode(
        rt,
        settings.secret_key,
        algorithms=[settings.algorithm],
    )
    assert decoded_access_token["sub"] == str(
        (
            await user_dao.get_user_by_username(
                username,
            )
        ).id,
    )
    assert (
        decoded_access_token["exp"] - decoded_access_token["iat"]
        == settings.access_token_expire_minutes * 60
    )
    # TODO: check scopes

    user_from_db: UserModel = await user_dao.get_user_by_username(
        username,
    )

    assert decoded_refresh_token["sub"] == str(
        user_from_db.id,
    )
    assert (
        decoded_refresh_token["exp"] - decoded_refresh_token["iat"]
        == settings.refresh_token_expire_minutes * 60
    )
    assert decoded_refresh_token["val"] == user.refresh_token_value


@pytest.mark.anyio
async def test_sign_in_invalid_password(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """
    Checks the register endpoint.

    :param client: client for the app.
    :param fastapi_app: current FastAPI application.
    """
    url = fastapi_app.url_path_for("login_for_access_token")
    username = "test"
    password = "aAZ?o2aaaaa"
    email = "test@test.com"

    await create_dummy_user(dbsession)
    user_dao = UserDAO(dbsession)
    user = await user_dao.get_user_by_username(username)
    if user is None:
        raise ValueError("User is None")
    await user_dao.update_active(-1 if user.id is None else user.id, True)

    response = await client.post(
        url,
        data={
            "username": username,
            "password": password + "a",
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.anyio
async def test_sign_in_inactive_user(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """
    Checks the register endpoint.

    :param client: client for the app.
    :param fastapi_app: current FastAPI application.
    """
    url = fastapi_app.url_path_for("login_for_access_token")
    username = "test"
    password = "aAZ?o2aaaaa"
    email = "test@test.com"

    await create_dummy_user(dbsession)
    user_dao = UserDAO(dbsession)
    user = await user_dao.get_user_by_username(username)
    if user is None:
        raise ValueError("User is None")
    await user_dao.update_active(-1 if user.id is None else user.id, False)

    response = await client.post(
        url,
        data={
            "username": username,
            "password": password,
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.anyio
async def test_sign_in_invalid_username(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """
    Checks the register endpoint.

    :param client: client for the app.
    :param fastapi_app: current FastAPI application.
    """
    url = fastapi_app.url_path_for("login_for_access_token")
    username = "test"
    password = "aAZ?o2aaaaa"
    email = "test@test.com"

    await create_dummy_user(dbsession)
    user_dao = UserDAO(dbsession)
    user = await user_dao.get_user_by_username(username)
    if user is None:
        raise ValueError("User is None")
    await user_dao.update_active(-1 if user.id is None else user.id, True)

    response = await client.post(
        url,
        data={
            "username": username + "a",
            "password": password,
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.anyio
async def test_sign_in_invalid_email(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """
    Checks the register endpoint.

    :param client: client for the app.
    :param fastapi_app: current FastAPI application.
    """
    url = fastapi_app.url_path_for("login_for_access_token")
    username = "test"
    password = "aAZ?o2aaaaa"
    email = "test@test.com"

    await create_dummy_user(dbsession)
    user_dao = UserDAO(dbsession)
    user = await user_dao.get_user_by_username(username)
    if user is None:
        raise ValueError("User is None")
    await user_dao.update_active(-1 if user.id is None else user.id, True)

    response = await client.post(
        url,
        data={
            "username": "a" + email,
            "password": password,
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


######################################################################
#                     TEST USER REFRESH TOKEN                        #
######################################################################


@pytest.mark.anyio
async def test_refresh_token(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """
    Checks the register endpoint.

    :param client: client for the app.
    :param fastapi_app: current FastAPI application.
    """
    url = fastapi_app.url_path_for("refresh_token_endpoint")
    username = "test"
    password = "aAZ?o2aaaaa"
    email = "test@test.com"

    await create_dummy_user(dbsession)
    user_dao = UserDAO(dbsession)
    user = await user_dao.get_user_by_username(username)
    if user is None:
        raise ValueError("User is None")
    await user_dao.update_active(user.id, True)

    refresh_token = await utils.create_refresh_token(user, user_dao)

    response = await client.post(
        url,
        json={
            "refresh_token": refresh_token,
        },
    )

    assert response.status_code == status.HTTP_200_OK
    at = response.json()["access_token"]
    assert at != ""
    rt = response.json()["refresh_token"]
    assert rt != ""
    assert response.json()["token_type"] == "Bearer"
    decoded_access_token = jwt.decode(
        at,
        settings.secret_key,
        algorithms=[settings.algorithm],
    )
    decoded_refresh_token = jwt.decode(
        rt,
        settings.secret_key,
        algorithms=[settings.algorithm],
    )
    assert decoded_access_token["sub"] == str(
        (
            await user_dao.get_user_by_username(
                username,
            )
        ).id,
    )
    assert (
        decoded_access_token["exp"] - decoded_access_token["iat"]
        == settings.access_token_expire_minutes * 60
    )
    # TODO: check scopes

    user_from_db: UserModel = await user_dao.get_user_by_username(
        username,
    )
    assert decoded_refresh_token["sub"] == str(
        user_from_db.id,
    )
    assert (
        decoded_refresh_token["exp"] - decoded_refresh_token["iat"]
        == settings.refresh_token_expire_minutes * 60
    )
    assert decoded_refresh_token["val"] == user.refresh_token_value


@pytest.mark.anyio
async def test_refresh_token_invalid_token(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """
    Checks the register endpoint.

    :param client: client for the app.
    :param fastapi_app: current FastAPI application.
    """
    url = fastapi_app.url_path_for("refresh_token_endpoint")
    username = "test"
    password = "aAZ?o2aaaaa"
    email = "test@test.com"

    await create_dummy_user(dbsession)
    user_dao = UserDAO(dbsession)
    user = await user_dao.get_user_by_username(username)
    if user is None:
        raise ValueError("User is None")
    await user_dao.update_active(-1 if user.id is None else user.id, True)

    refresh_token = await utils.create_refresh_token(user, user_dao)

    response = await client.post(
        url,
        json={
            "refresh_token": refresh_token + "a",
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.anyio
async def test_refresh_token_expired_token(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
    monkeypatch: MonkeyPatch,
) -> None:
    """
    Checks the register endpoint.

    :param client: client for the app.
    :param fastapi_app: current FastAPI application.
    """
    url = fastapi_app.url_path_for("refresh_token_endpoint")
    username = "test"
    password = "aAZ?o2aaaaa"
    email = "test@test.com"

    await create_dummy_user(dbsession)
    user_dao = UserDAO(dbsession)
    user = await user_dao.get_user_by_username(username)
    if user is None:
        raise ValueError("User is None")
    await user_dao.update_active(-1 if user.id is None else user.id, True)

    refresh_token = await utils.create_refresh_token(user, user_dao)

    expire_time = datetime.datetime.utcnow() + datetime.timedelta(
        minutes=settings.refresh_token_expire_minutes + 1,
    )

    monkeypatch.setattr(utils, "now", lambda: expire_time)

    response = await client.post(
        url,
        json={
            "refresh_token": refresh_token,
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.anyio
async def test_refresh_token_user_not_have_token(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """
    Checks the register endpoint.

    :param client: client for the app.
    :param fastapi_app: current FastAPI application.
    """
    url = fastapi_app.url_path_for("refresh_token_endpoint")
    username = "test"
    password = "aAZ?o2aaaaa"
    email = "test@test.com"

    await create_dummy_user(dbsession)
    user_dao = UserDAO(dbsession)
    user = await user_dao.get_user_by_username(username)
    if user is None:
        raise ValueError("User is None")
    await user_dao.update_active(-1 if user.id is None else user.id, True)

    response = await client.post(
        url,
        json={
            "refresh_token": "a",
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.anyio
async def test_refresh_token_stolen(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """
    Checks the register endpoint.

    :param client: client for the app.
    :param fastapi_app: current FastAPI application.
    """
    url = fastapi_app.url_path_for("refresh_token_endpoint")
    username = "test"
    password = "aAZ?o2aaaaa"
    email = "test@test.com"

    await create_dummy_user(dbsession)
    user_dao = UserDAO(dbsession)
    user = await user_dao.get_user_by_username(username)
    if user is None:
        raise ValueError("User is None")
    await user_dao.update_active(-1 if user.id is None else user.id, True)

    refresh_token = await utils.create_refresh_token(user, user_dao)

    response = await client.post(
        url,
        json={
            "refresh_token": refresh_token,
        },
    )

    assert response.status_code == status.HTTP_200_OK
    new_rt = response.json()["refresh_token"]

    response = await client.post(
        url,
        json={
            "refresh_token": refresh_token,
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert user.refresh_token_value is None

    response = await client.post(
        url,
        json={
            "refresh_token": new_rt,
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
