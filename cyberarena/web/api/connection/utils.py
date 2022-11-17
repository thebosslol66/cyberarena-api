from typing import Any, Callable, Dict, Optional

from fastapi import Depends
from typing_extensions import Coroutine

from cyberarena.db.dao.user_dao import UserDAO
from cyberarena.web.api.connection.schema import SignUpStatusDTO


class VerifyUserModel(object):
    """User model for verification."""

    def __init__(
        self,
        username: str,
        password: str,
        email: str,
        user_dao: UserDAO = Depends(),
    ) -> None:
        self.username = username
        self.password = password
        self.email = email
        self.user_dao = user_dao


async def is_username_correct(user_model: VerifyUserModel) -> Optional[str]:
    """
    Verify if username is correct.

    :param user_model: User model.
    :return: True if username is correct, otherwise return the error message.
    """
    if len(user_model.username) < 4:
        return "Username is too short"
    if not any(char.isalnum() for char in user_model.username):
        return "Username must contain only alphanumeric character"
    if not any(not char.isspace() for char in user_model.username):
        return "Username must not contain spaces"
    return None


async def is_password_correct(user_model: VerifyUserModel) -> Optional[str]:
    """
    Verify if password is correct.

    :param user_model: User model.
    :return: True if password is correct, otherwise return the error message.
    """
    verification_responses: Dict[Callable[[str], bool], str] = {
        lambda char: char.isdigit(): "Password must contain at least one digit",
        lambda char: char.isalpha(): "Password must contain at least one letter",
        lambda char: char.islower(): "Password must contain at"
        " least one lowercase letter",
        lambda char: char.isupper(): "Password must contain at"
        " least one uppercase letter",
        lambda char: not char.isspace(): "Password must not contain spaces",
        lambda char: not char.isalnum(): "Password must contain at"
        " least one alphanumeric character",
    }

    if len(user_model.password) < 8:
        return "Password is too short"
    for verification_function, response in verification_responses.items():
        if not any(verification_function(char) for char in user_model.password):
            return response
    return None


async def is_email_correct(user_model: VerifyUserModel) -> Optional[str]:
    """
    Verify if email is correct.

    :param user_model: User model.
    :return: True if email is correct, otherwise return the error message.
    """
    if not any(char == "@" for char in user_model.email):
        return "Email must contain @ character"
    if not any(char == "." for char in user_model.email):
        return "Email must contain . character"
    return None


async def is_username_taken(user_model: VerifyUserModel) -> Optional[str]:
    """
    Verify if username is taken.

    :param user_model: User model.
    :return: True if username is taken, otherwise return the error message.
    """
    user = await user_model.user_dao.get_user_by_username(user_model.username)
    if user:
        return "Username already exists"
    return None


async def is_email_taken(user_model: VerifyUserModel) -> Optional[str]:
    """
    Verify if email is taken.

    :param user_model: User model.
    :return: True if email is taken, otherwise return the error message.
    """
    user = await user_model.user_dao.get_user_by_email(user_model.email)
    if user:
        return "Email already exists"
    return None


async def verify_user_sign_in(
    username: str,
    password: str,
    email: str,
    user_dao: UserDAO,
) -> SignUpStatusDTO:
    """
    Verify if user can sign in.

    :param user_dao: DAO for user models.
    :param username: username of user.
    :param password: password of user.
    :param email: email of user.
    :return: True if user can sign in, otherwise return the error message.
    """
    verifications_responses: Dict[  # noqa: WPS234
        Callable[
            [VerifyUserModel],
            Coroutine[Any, Any, Optional[str]],
        ],
        int,
    ] = {
        is_username_correct: 1,
        is_password_correct: 2,
        is_email_correct: 3,
        is_username_taken: 4,
        is_email_taken: 5,
    }

    user_model = VerifyUserModel(username, password, email, user_dao)

    for verification, response in verifications_responses.items():
        verification_response = await verification(
            user_model,
        )
        if verification_response:
            return SignUpStatusDTO(
                status=response,
                message=verification_response,
            )

    return SignUpStatusDTO(status=0, message="")
