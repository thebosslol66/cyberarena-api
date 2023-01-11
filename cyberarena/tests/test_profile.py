# flake8: noqa
import os
import shutil
from typing import Callable

import pytest
from _pytest.monkeypatch import MonkeyPatch
from fastapi import Depends, FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from cyberarena.db.dao.user_dao import UserDAO
from cyberarena.db.models.user_model import UserModel
from cyberarena.settings import settings
from cyberarena.web.api.connection.utils import get_current_user


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


######################################################################
#                     TESTS USER INFORMATIONS                        #
######################################################################


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


@pytest.mark.anyio
async def test_get_current_user_profile(
    fastapi_app: FastAPI,
    client: AsyncClient,
    monkeypatch: MonkeyPatch,
    dbsession: AsyncSession,
) -> None:
    """
    Test get current user profile.

    :param app: fastapi app.
    :param client: httpx client.
    :param monkeypatch: monkeypatch.
    :param dbsession: database session.
    """
    username = "test"
    await create_dummy_user(dbsession)
    dao = UserDAO(dbsession)

    fastapi_app.dependency_overrides[get_current_user] = override_get_current_user(
        username,
    )

    response = await client.get(
        fastapi_app.url_path_for("get_current_user_profile"),
    )
    print(response.json())
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "username": "test",
        "email": "test@test.com",
        "active": False,
    }


######################################################################
#                     TESTS USER INFORMATIONS                        #
######################################################################


@pytest.mark.anyio
async def test_get_specified_user_profile(
    fastapi_app: FastAPI,
    client: AsyncClient,
    monkeypatch: MonkeyPatch,
    dbsession: AsyncSession,
) -> None:
    """
    Test get current user profile.

    :param fastapi_app: fastapi app.
    :param client: httpx client.
    :param monkeypatch: monkeypatch.
    :param dbsession: database session.
    """
    username = "test"
    await create_dummy_user(dbsession)
    dao = UserDAO(dbsession)

    fastapi_app.dependency_overrides[get_current_user] = override_get_current_user(
        username,
    )

    response = await client.get(
        fastapi_app.url_path_for("get_specified_user_profile", username=username),
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.anyio
async def test_get_specified_user_profile_user_not_exist(
    fastapi_app: FastAPI,
    client: AsyncClient,
    monkeypatch: MonkeyPatch,
    dbsession: AsyncSession,
) -> None:
    """
    Test get current user profile.

    :param fastapi_app: fastapi app.
    :param client: httpx client.
    :param monkeypatch: monkeypatch.
    :param dbsession: database session.
    """
    username = "test"
    await create_dummy_user(dbsession)
    dao = UserDAO(dbsession)

    fastapi_app.dependency_overrides[get_current_user] = override_get_current_user(
        username,
    )

    response = await client.get(
        fastapi_app.url_path_for("get_specified_user_profile", username="test2"),
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "User not found",
    }


######################################################################
#                     TESTS CHANGE PASSWORD                          #
######################################################################


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
    new_password = "aAZ?o2aaaaaa"

    await create_dummy_user(dbsession)
    dao = UserDAO(dbsession)

    fastapi_app.dependency_overrides[get_current_user] = override_get_current_user(
        username,
    )

    url = fastapi_app.url_path_for("change_password")
    response = await client.put(
        url,
        json={
            "password": password,
            "new_setting": new_password,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    user = await dao.get_user_by_username(username)
    assert not user.is_correct_password(password)
    assert user.is_correct_password(new_password)


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
    dao = UserDAO(dbsession)

    url = fastapi_app.url_path_for("change_password")
    response = await client.put(
        url,
        json={
            "password": password,
            "new_setting": new_password,
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    user = await dao.get_user_by_username(username)
    assert user.is_correct_password(password)


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

    dao = UserDAO(dbsession)

    fastapi_app.dependency_overrides[get_current_user] = override_get_current_user(
        username,
    )

    url = fastapi_app.url_path_for("change_password")
    response = await client.put(
        url,
        json={
            "password": wrong_password,
            "new_setting": new_password,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    user = await dao.get_user_by_username(username)
    assert user.is_correct_password(password)


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
    dao = UserDAO(dbsession)

    fastapi_app.dependency_overrides[get_current_user] = override_get_current_user(
        username,
    )

    url = fastapi_app.url_path_for("change_password")
    response = await client.put(
        url,
        json={
            "password": password,
            "new_setting": password,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    user = await dao.get_user_by_username(username)
    assert user.is_correct_password(password)


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
    dao = UserDAO(dbsession)

    fastapi_app.dependency_overrides[get_current_user] = override_get_current_user(
        username,
    )

    url = fastapi_app.url_path_for("change_password")
    for new_password in new_passwords:
        response = await client.put(
            url,
            json={
                "password": password,
                "new_setting": new_password,
            },
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        user = await dao.get_user_by_username(username)
        assert user.is_correct_password(password)


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
    dao = UserDAO(dbsession)

    fastapi_app.dependency_overrides[get_current_user] = override_get_current_user(
        username,
    )

    url = fastapi_app.url_path_for("change_email")
    response = await client.put(
        url,
        json={
            "password": password,
            "new_setting": new_email,
        },
    )
    assert response.status_code == status.HTTP_200_OK
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
    dao = UserDAO(dbsession)

    url = fastapi_app.url_path_for("change_email")
    response = await client.put(
        url,
        json={
            "password": password,
            "new_setting": new_email,
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
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
    wrong_password = "aAZ?o2aaaaaa"
    old_email = "test@test.com"
    new_email = "test2@test.com"

    await create_dummy_user(dbsession)
    dao = UserDAO(dbsession)

    fastapi_app.dependency_overrides[get_current_user] = override_get_current_user(
        username,
    )

    url = fastapi_app.url_path_for("change_email")
    response = await client.put(
        url,
        json={
            "password": wrong_password,
            "new_setting": new_email,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
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
    dao = UserDAO(dbsession)

    fastapi_app.dependency_overrides[get_current_user] = override_get_current_user(
        username,
    )

    url = fastapi_app.url_path_for("change_email")
    response = await client.put(
        url,
        json={
            "password": password,
            "new_setting": old_email,
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
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
    dao = UserDAO(dbsession)

    fastapi_app.dependency_overrides[get_current_user] = override_get_current_user(
        username,
    )

    url = fastapi_app.url_path_for("change_email")
    for wrong_email in wrong_emails:
        response = await client.put(
            url,
            json={
                "password": password,
                "new_setting": wrong_email,
            },
        )
        print(wrong_email)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
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
    dao = UserDAO(dbsession)

    fastapi_app.dependency_overrides[get_current_user] = override_get_current_user(
        username,
    )

    url = fastapi_app.url_path_for("change_email")
    response = await client.put(
        url,
        json={
            "password": password,
            "new_setting": new_email,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    user = await dao.get_user_by_username(username)
    assert user.email != new_email


######################################################################
#                      TESTS CHANGE USERNAME                         #
######################################################################


@pytest.mark.anyio
async def test_change_username(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
    monkeypatch: MonkeyPatch,
) -> None:
    """Tests change username."""

    username = "test"
    password = "aAZ?o2aaaaa"
    new_username = "test2"

    await create_dummy_user(dbsession)
    dao = UserDAO(dbsession)

    fastapi_app.dependency_overrides[get_current_user] = override_get_current_user(
        username,
    )

    url = fastapi_app.url_path_for("change_username")
    response = await client.put(
        url,
        json={
            "password": password,
            "new_setting": new_username,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    user = await dao.get_user_by_username(new_username)
    assert user.username == new_username


@pytest.mark.anyio
async def test_change_username_wrong_password(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
    monkeypatch: MonkeyPatch,
) -> None:
    """Tests change username with wrong password."""
    username = "test"
    password = "aAZ?o2aaaaa"
    new_username = "test2"

    await create_dummy_user(dbsession)
    dao = UserDAO(dbsession)

    fastapi_app.dependency_overrides[get_current_user] = override_get_current_user(
        username,
    )

    url = fastapi_app.url_path_for("change_username")
    response = await client.put(
        url,
        json={
            "password": "wrong_password",
            "new_setting": new_username,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    user = await dao.get_user_by_username(username)
    assert user.username == username


@pytest.mark.anyio
async def test_change_username_same_username(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
    monkeypatch: MonkeyPatch,
) -> None:
    """Tests change username with same username."""
    username = "test"
    password = "aAZ?o2aaaaa"

    await create_dummy_user(dbsession)
    dao = UserDAO(dbsession)

    fastapi_app.dependency_overrides[get_current_user] = override_get_current_user(
        username,
    )

    url = fastapi_app.url_path_for("change_username")
    response = await client.put(
        url,
        json={
            "password": password,
            "new_setting": username,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    user = await dao.get_user_by_username(username)
    assert user.username == username


@pytest.mark.anyio
async def test_change_username_other_account_have_same_username(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
    monkeypatch: MonkeyPatch,
) -> None:
    """Tests change username with other account have same username."""
    username = "test"
    password = "aAZ?o2aaaaa"
    new_username = "test2"

    await create_dummy_user(dbsession)
    await create_dummy_user(dbsession, username=new_username, email="test2@test.com")
    dao = UserDAO(dbsession)

    fastapi_app.dependency_overrides[get_current_user] = override_get_current_user(
        username,
    )

    url = fastapi_app.url_path_for("change_username")
    response = await client.put(
        url,
        json={
            "password": password,
            "new_setting": new_username,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    user = await dao.get_user_by_username(username)
    assert user.username == username


######################################################################
#                       TESTS CHANGE AVATAR                          #
######################################################################


@pytest.fixture
def erease_avatar_file() -> None:  # pragma: no cover
    """Fixture to delete avatar file."""
    yield
    for file in os.listdir(settings.avatar_path):
        os.remove(os.path.join(settings.avatar_path, file))


def verify_avatar_file(filename: str) -> bool:
    """Verify if avatar file exists."""
    return os.path.exists(os.path.join(settings.avatar_path, filename))


@pytest.mark.anyio
async def test_change_avatar(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
    monkeypatch: MonkeyPatch,
    image_diff: Callable,
) -> None:
    """Tests change avatar."""
    username = "test"

    await create_dummy_user(dbsession)
    dao = UserDAO(dbsession)

    fastapi_app.dependency_overrides[get_current_user] = override_get_current_user(
        username,
    )

    url = fastapi_app.url_path_for("change_avatar")

    response = await client.put(
        url,
        files={
            "avatar_img": open(
                "cyberarena/tests_data/imgs/test_avatar_good_512x512.png",
                "rb",
            ),
        },
    )
    print(response.json())
    assert response.status_code == status.HTTP_200_OK
    user = await dao.get_user_by_username(username)
    assert verify_avatar_file(str(user.id) + ".png")
    assert image_diff(
        "cyberarena/tests_data/imgs/test_avatar_good_512x512.png",
        os.path.join(settings.avatar_path, str(user.id) + ".png"),
    )


@pytest.mark.anyio
async def test_change_avatar_good_jpg(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
    monkeypatch: MonkeyPatch,
    image_diff: Callable,
) -> None:
    """Tests change avatar with good jpg."""
    username = "test"

    await create_dummy_user(dbsession)
    dao = UserDAO(dbsession)

    fastapi_app.dependency_overrides[get_current_user] = override_get_current_user(
        username,
    )

    url = fastapi_app.url_path_for("change_avatar")

    response = await client.put(
        url,
        files={
            "avatar_img": open(
                "cyberarena/tests_data/imgs/test_avatar_good_512x512.jpg",
                "rb",
            ),
        },
    )

    assert response.status_code == status.HTTP_200_OK
    user = await dao.get_user_by_username(username)
    assert verify_avatar_file(str(user.id) + ".png")
    assert image_diff(
        "cyberarena/tests_data/imgs/test_avatar_good_512x512.jpg",
        os.path.join(settings.avatar_path, str(user.id) + ".png"),
    )


@pytest.mark.anyio
async def test_change_avatar_false_png(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
    monkeypatch: MonkeyPatch,
) -> None:
    """Test change avatar with a jfif image rename with png at end"""
    username = "test"

    await create_dummy_user(dbsession)
    dao = UserDAO(dbsession)

    fastapi_app.dependency_overrides[get_current_user] = override_get_current_user(
        username,
    )

    url = fastapi_app.url_path_for("change_avatar")

    response = await client.put(
        url,
        files={
            "avatar_img": open(
                "cyberarena/tests_data/imgs/test_avatar_false_png_512x512.png",
                "rb",
            ),
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    user = await dao.get_user_by_username(username)
    assert not verify_avatar_file(str(user.id) + ".png")


@pytest.mark.anyio
async def test_change_avatar_too_large(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
    monkeypatch: MonkeyPatch,
) -> None:
    """Tests change avatar to large."""
    username = "test"

    await create_dummy_user(dbsession)
    dao = UserDAO(dbsession)

    fastapi_app.dependency_overrides[get_current_user] = override_get_current_user(
        username,
    )

    url = fastapi_app.url_path_for("change_avatar")

    response = await client.put(
        url,
        files={
            "avatar_img": open(
                "cyberarena/tests_data/imgs/test_avatar_bad_618x769.jpg",
                "rb",
            ),
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    user = await dao.get_user_by_username(username)
    assert not verify_avatar_file(str(user.id) + ".png")


@pytest.mark.anyio
async def test_change_avatar_bad_format(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
    monkeypatch: MonkeyPatch,
) -> None:
    """Tests change avatar with bad format."""
    username = "test"

    await create_dummy_user(dbsession)
    dao = UserDAO(dbsession)

    fastapi_app.dependency_overrides[get_current_user] = override_get_current_user(
        username,
    )

    url = fastapi_app.url_path_for("change_avatar")

    response = await client.put(
        url,
        files={
            "avatar_img": open(
                "cyberarena/tests_data/imgs/test_avatar_bad_format_512x512.gif",
                "rb",
            ),
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    user = await dao.get_user_by_username(username)
    assert not verify_avatar_file(str(user.id) + ".png")


@pytest.mark.anyio
async def test_change_avatar_lower_size(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
    monkeypatch: MonkeyPatch,
    image_diff: Callable,
) -> None:
    """Tests change avatar with an image < 512x512."""
    username = "test"

    await create_dummy_user(dbsession)
    dao = UserDAO(dbsession)

    fastapi_app.dependency_overrides[get_current_user] = override_get_current_user(
        username,
    )

    url = fastapi_app.url_path_for("change_avatar")

    response = await client.put(
        url,
        files={
            "avatar_img": open(
                "cyberarena/tests_data/imgs/test_avatar_good_453x292.png",
                "rb",
            ),
        },
    )

    assert response.status_code == status.HTTP_200_OK
    user = await dao.get_user_by_username(username)
    assert verify_avatar_file(str(user.id) + ".png")
    assert image_diff(
        "cyberarena/tests_data/imgs/test_avatar_good_453x292.png",
        os.path.join(settings.avatar_path, str(user.id) + ".png"),
    )


@pytest.mark.anyio
async def test_change_avatar_with_RGBA_field(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
    monkeypatch: MonkeyPatch,
    image_diff: Callable,
) -> None:
    """Tests change avatar with an image with RGBA field."""
    username = "test"

    await create_dummy_user(dbsession)
    dao = UserDAO(dbsession)

    fastapi_app.dependency_overrides[get_current_user] = override_get_current_user(
        username,
    )

    url = fastapi_app.url_path_for("change_avatar")

    response = await client.put(
        url,
        files={
            "avatar_img": open(
                "cyberarena/tests_data/imgs/test_avatar_good_RGBA_512x512.png",
                "rb",
            ),
        },
    )

    assert response.status_code == status.HTTP_200_OK
    user = await dao.get_user_by_username(username)
    assert verify_avatar_file(str(user.id) + ".png")
    assert image_diff(
        "cyberarena/tests_data/imgs/test_avatar_good_RGBA_512x512.png",
        os.path.join(settings.avatar_path, str(user.id) + ".png"),
    )


@pytest.mark.anyio
async def test_change_avatar_good_dimentions_but_bigger(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
    monkeypatch: MonkeyPatch,
) -> None:
    """Tests change avatar with an image > 1Mo."""
    username = "test"

    await create_dummy_user(dbsession)
    dao = UserDAO(dbsession)

    fastapi_app.dependency_overrides[get_current_user] = override_get_current_user(
        username,
    )

    url = fastapi_app.url_path_for("change_avatar")

    response = await client.put(
        url,
        files={
            "avatar_img": open(
                "cyberarena/tests_data/imgs/test_avatar_bad_too_big_512x512.png",
                "rb",
            ),
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    user = await dao.get_user_by_username(username)
    assert not verify_avatar_file(str(user.id) + ".png")


@pytest.mark.anyio
async def test_change_avatar_with_already_avatar_set(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
    monkeypatch: MonkeyPatch,
    image_diff: Callable,
) -> None:
    """Tests change avatar with an avatar already set."""
    username = "test"

    await create_dummy_user(dbsession)
    dao = UserDAO(dbsession)

    fastapi_app.dependency_overrides[get_current_user] = override_get_current_user(
        username,
    )

    user = await dao.get_user_by_username(username)

    # copy a good image to the avatar folder
    shutil.copy(
        "cyberarena/tests_data/imgs/test_avatar_good_512x512.png",
        os.path.join(settings.avatar_path, str(user.id) + ".png"),
    )

    url = fastapi_app.url_path_for("change_avatar")

    response = await client.put(
        url,
        files={
            "avatar_img": open(
                "cyberarena/tests_data/imgs/test_avatar_good_512x512.jpg",
                "rb",
            ),
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert verify_avatar_file(str(user.id) + ".png")

    # TODO: fix this test

    assert image_diff(
        "cyberarena/tests_data/imgs/test_avatar_good_512x512.jpg",
        os.path.join(settings.avatar_path, str(user.id) + ".png"),
        throw_exception=False,
    )


@pytest.mark.anyio
async def test_change_avatar_replace_with_bad_dont_change_the_old(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
    monkeypatch: MonkeyPatch,
    image_diff: Callable,
) -> None:
    """Tests change avatar with an avatar already set."""
    username = "test"

    await create_dummy_user(dbsession)
    dao = UserDAO(dbsession)

    fastapi_app.dependency_overrides[get_current_user] = override_get_current_user(
        username,
    )

    user = await dao.get_user_by_username(username)

    # copy a good image to the avatar folder
    shutil.copy(
        "cyberarena/tests_data/imgs/test_avatar_good_512x512.png",
        os.path.join(settings.avatar_path, str(user.id) + ".png"),
    )

    url = fastapi_app.url_path_for("change_avatar")

    response = await client.put(
        url,
        files={
            "avatar_img": open(
                "cyberarena/tests_data/imgs/test_avatar_bad_format_512x512.gif",
                "rb",
            ),
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert verify_avatar_file(str(user.id) + ".png")
    assert image_diff(
        "cyberarena/tests_data/imgs/test_avatar_good_512x512.png",
        os.path.join(settings.avatar_path, str(user.id) + ".png"),
        throw_exception=False,
    )


######################################################################
#                         TESTS ME AVATAR                            #
######################################################################


@pytest.mark.anyio
async def test_get_me_avatar(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
    monkeypatch: MonkeyPatch,
) -> None:
    """Tests get me avatar."""
    username = "test"

    await create_dummy_user(dbsession)
    dao = UserDAO(dbsession)

    fastapi_app.dependency_overrides[get_current_user] = override_get_current_user(
        username,
    )

    user = await dao.get_user_by_username(username)

    # copy a good image to the avatar folder
    shutil.copy(
        "cyberarena/tests_data/imgs/test_avatar_good_512x512.png",
        os.path.join(settings.avatar_path, str(user.id) + ".png"),
    )

    url = fastapi_app.url_path_for("get_current_user_avatar")

    response = await client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.headers["content-type"] == "image/png"
    assert (
        response.content
        == open(
            "cyberarena/tests_data/imgs/test_avatar_good_512x512.png",
            "rb",
        ).read()
    )


@pytest.mark.anyio
async def test_get_me_avatar_no_avatar_set(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
    monkeypatch: MonkeyPatch,
) -> None:
    """Tests get me avatar."""
    username = "test"

    await create_dummy_user(dbsession)
    dao = UserDAO(dbsession)

    fastapi_app.dependency_overrides[get_current_user] = override_get_current_user(
        username,
    )

    user = await dao.get_user_by_username(username)
    url = fastapi_app.url_path_for("get_current_user_avatar")

    response = await client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.headers["content-type"] == "image/png"
    assert (
        response.content
        == open(
            os.path.join(
                settings.avatar_path,
                "default",
                str(
                    (
                        user.id
                        % len(
                            os.listdir(
                                os.path.join(settings.avatar_path, "default"),
                            ),
                        )
                    )
                    + 1,
                )
                + ".png",
            ),
            "rb",
        ).read()
    )


@pytest.mark.anyio
async def test_get_me_avatar_protected(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
    monkeypatch: MonkeyPatch,
) -> None:
    """Tests get me avatar."""
    username = "test"

    await create_dummy_user(dbsession)
    dao = UserDAO(dbsession)

    user = await dao.get_user_by_username(username)
    url = fastapi_app.url_path_for("get_current_user_avatar")

    response = await client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


######################################################################
#                      TESTS USERNAME AVATAR                         #
######################################################################


@pytest.mark.anyio
async def test_get_username_avatar(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
    monkeypatch: MonkeyPatch,
) -> None:
    """Tests get username avatar."""
    username = "test"

    await create_dummy_user(dbsession)
    dao = UserDAO(dbsession)

    user = await dao.get_user_by_username(username)

    # copy a good image to the avatar folder
    shutil.copy(
        "cyberarena/tests_data/imgs/test_avatar_good_512x512.png",
        os.path.join(settings.avatar_path, str(user.id) + ".png"),
    )

    url = fastapi_app.url_path_for("get_specified_user_avatar", username=username)

    response = await client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.headers["content-type"] == "image/png"
    assert (
        response.content
        == open(
            "cyberarena/tests_data/imgs/test_avatar_good_512x512.png",
            "rb",
        ).read()
    )


@pytest.mark.anyio
async def test_get_username_avatar_no_avatar_set(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
    monkeypatch: MonkeyPatch,
) -> None:
    """Tests get username avatar."""
    username = "test"

    await create_dummy_user(dbsession)
    dao = UserDAO(dbsession)

    user = await dao.get_user_by_username(username)

    url = fastapi_app.url_path_for("get_specified_user_avatar", username=username)

    response = await client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.headers["content-type"] == "image/png"
    assert (
        response.content
        == open(
            os.path.join(
                settings.avatar_path,
                "default",
                str(
                    (
                        user.id
                        % len(
                            os.listdir(
                                os.path.join(settings.avatar_path, "default"),
                            ),
                        )
                    )
                    + 1,
                )
                + ".png",
            ),
            "rb",
        ).read()
    )


@pytest.mark.anyio
async def test_get_username_avatar_user_not_exist(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
    monkeypatch: MonkeyPatch,
) -> None:
    """Tests get username avatar."""
    username = "test"

    await create_dummy_user(dbsession)
    dao = UserDAO(dbsession)

    user = await dao.get_user_by_username(username)

    url = fastapi_app.url_path_for("get_specified_user_avatar", username="test2")

    response = await client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
