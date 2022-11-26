import uuid
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import JWTError, jwt
from pydantic import ValidationError
from starlette import status
from typing_extensions import Coroutine

from cyberarena.db.dao.user_dao import UserDAO
from cyberarena.db.models.user_model import UserModel
from cyberarena.settings import settings
from cyberarena.web.api.connection.schema import SignUpStatusDTO, TokenData


def now() -> datetime:
    """
    Get current time.

    :return: Current time.
    """
    return datetime.utcnow()


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


async def autenticate_user(
    username: str,
    password: str,
    user_dao: UserDAO,
) -> Optional[UserModel]:
    """
    Authenticate user.

    :param user_dao: DAO for user models.
    :param username: username of user.
    :param password: password of user.
    :return: Token if user is authenticated, otherwise return None
    """
    user = await user_dao.get_user_by_username(username)
    if not user:
        user = await user_dao.get_user_by_email(username)
    if not user:
        return None
    if not user.is_correct_password(password):
        return None
    return user


async def create_access_token(user: UserModel, scopes: str) -> str:
    """
    Create access token.

    :param user: User model.
    :param scopes: Scopes of token.
    :return: Access token.
    """
    creation_time = now()
    return jwt.encode(
        {
            "sub": str(user.id),
            "iat": creation_time,
            "exp": creation_time
            + timedelta(
                minutes=settings.access_token_expire_minutes,
            ),
            "scopes": scopes,
        },
        settings.secret_key,
        algorithm=settings.algorithm,
    )


async def create_refresh_token(user: UserModel, user_dao: UserDAO) -> str:
    """
    Create refresh token.

    :param user: User model that exist in db.
    :param user_dao: DAO for user models.
    :return: Refresh token.
    """
    creation_time = now()
    value = uuid.uuid4().hex

    await user_dao.update_refresh_token(0 if user.id is None else user.id, value)
    return jwt.encode(
        {
            "sub": str(user.id),
            "val": value,
            "iat": creation_time,
            "exp": creation_time
            + timedelta(
                minutes=settings.refresh_token_expire_minutes,
            ),
        },
        settings.secret_key,
        algorithm=settings.algorithm,
    )


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="sign/token",
    scopes={},
)


async def verify_payload_at(
    payload: Any,
    credentials_exception: HTTPException,
) -> TokenData:
    """
    Verify payload at.

    :param payload: Payload.
    :param credentials_exception: Exception.
    :return: Token data.
    :raises credentials_exception: If token is invalid.
    """
    user_id: int = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    token_scopes: str = payload.get("scopes", "")
    return TokenData(scopes=token_scopes, user_id=user_id)


async def get_current_user(  # noqa: C901
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme),
    user_dao: UserDAO = Depends(),
) -> UserModel:
    """
    Get current user from an acess token.

    :param security_scopes: Scopes of token.
    :param token: Token.
    :param user_dao: DAO for user models.
    :return: Current user.
    :raises credentials_exception: If token is invalid.
    :raises HTTPException: If token is expired.
    """
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        result: TokenData = await verify_payload_at(
            jwt.decode(
                token,
                settings.secret_key,
                algorithms=[settings.algorithm],
            ),
            credentials_exception,
        )

    except (JWTError, ValidationError):  # noqa: WPS329
        raise credentials_exception
    user = await user_dao.get_user_by_id(result.user_id)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in result.scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


class _PayloadValueForTranmissionRT(object):
    """
    Payload value for transmission.

    It is useless for anything else than to be transmitted between, this two functions.

    :param value: Value of payload.
    :param refresh_token_value: Value of refresh token.
    """

    def __init__(self, user_id: int, refresh_token_value: str) -> None:
        """
        Initialize PayloadValueForTranmission.

        :param user_id: Id of user.
        :param refresh_token_value: Value of refresh token.
        """
        self.user_id = user_id
        self.refresh_token_value = refresh_token_value

    user_id: int
    refresh_token_value: str


async def _verify_payload_rt(
    payload: Any,
    credentials_exception: HTTPException,
) -> _PayloadValueForTranmissionRT:
    """
    Verify payload.

    :param payload: Payload of token.
    :param credentials_exception: Exception to raise if payload is invalid.
    :raises credentials_exception: If payload is invalid.
    :return: True if payload is valid, otherwise return False.
    """
    user_id: int = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    expires = payload.get("exp", 0)
    if expires < now().timestamp():
        raise credentials_exception
    refresh_token = payload.get("val")
    if refresh_token is None:
        raise credentials_exception
    return _PayloadValueForTranmissionRT(user_id, refresh_token)


async def get_curent_user_with_refresh_token(
    token: str,
    user_dao: UserDAO = Depends(),
) -> UserModel:
    """
    Get current user from a refresh token.

    :param token: Token.
    :param user_dao: DAO for user models.
    :return: Current user.
    :raises credentials_exception: If token is invalid.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        result: _PayloadValueForTranmissionRT = await _verify_payload_rt(
            jwt.decode(
                token,
                settings.secret_key,
                algorithms=[settings.algorithm],
            ),
            credentials_exception,
        )
    except (JWTError, ValidationError):  # noqa: WPS329
        raise credentials_exception
    user = await user_dao.get_user_by_id(result.user_id)
    if user is None:
        raise credentials_exception
    if result.refresh_token_value != user.refresh_token_value:
        await user_dao.update_refresh_token(result.user_id, None)
        raise credentials_exception
    return user
