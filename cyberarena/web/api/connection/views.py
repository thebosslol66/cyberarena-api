from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from cyberarena.db.dao.user_dao import UserDAO
from cyberarena.db.models.user_model import UserModel
from cyberarena.settings import settings
from cyberarena.web.api.connection.schema import (
    AskNewTokenData,
    SignUpData,
    SignUpStatusDTO,
    Tokens,
)
from cyberarena.web.api.connection.utils import (
    autenticate_user,
    create_access_token,
    create_refresh_token,
    get_curent_user_with_refresh_token,
    verify_user_sign_in,
)

router = APIRouter()


@router.post("/sign-up", response_model=SignUpStatusDTO)
async def sign_up(
    sign_up_data: SignUpData,
    user_dao: UserDAO = Depends(),
) -> SignUpStatusDTO:
    """
    Sign up user.

    :param sign_up_data: data for sign up.
    :param user_dao: user dao.
    :return: status of sign up.
    """
    response = await verify_user_sign_in(
        sign_up_data.username,
        sign_up_data.password,
        sign_up_data.email,
        user_dao,
    )
    # Create user
    if response.status == 0:
        await user_dao.create_user(
            sign_up_data.username,
            sign_up_data.email,
            sign_up_data.password,
        )
        response.message = "User created"
    # TODO: remove this to active the account later by email
    await set_user_active(sign_up_data.username, user_dao)
    return response


@router.get("/activate")
async def set_user_active(
    username: str,
    user_dao: UserDAO = Depends(),
) -> None:
    """
    Activate user.

    :param username: name of user.
    :param user_dao: user dao.
    """
    user: Optional[UserModel] = await user_dao.get_user_by_username(username)
    if user is not None and user.id is not None:
        await user_dao.update_active(user.id, active=True)


@router.post("/token", response_model=Tokens)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_dao: UserDAO = Depends(),
) -> Tokens:
    """
    Send user credentials to get back access token and refresh token.

    :param form_data: data from form.
    :param user_dao: user dao.
    :return: tokens.
    :raises HTTPException: if user is not active or credentials are wrong.
    """
    user: Optional[UserModel] = await autenticate_user(
        form_data.username,
        form_data.password,
        user_dao,
    )
    if not user:
        raise HTTPException(
            status_code=400,  # noqa: WPS432
            detail="Incorrect username or password",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=400,  # noqa: WPS432
            detail="Inactive user",
        )
    user.last_login = datetime.now()
    access_token = await create_access_token(user, "")  # TODO: add scopes from user db
    if settings.environment == "dev":
        access_token = await create_access_token(user, " ".join(form_data.scopes))

    refresh_token = await create_refresh_token(user, user_dao)
    return Tokens(  # noqa: S106
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="Bearer",
        expires=settings.access_token_expire_minutes * 60,
    )


@router.post("/refresh-token", response_model=Tokens)
async def refresh_token_endpoint(
    ask_new_tokens: AskNewTokenData,
    user_dao: UserDAO = Depends(),
) -> Tokens:
    """
    Refresh token endpoint.

    :param ask_new_tokens: data for refresh token.
    :param user_dao: user dao.
    :return: new tokens.
    :raises HTTPException: if user is not active.
    """
    user = await get_curent_user_with_refresh_token(
        ask_new_tokens.refresh_token,
        user_dao,
    )
    if not user:
        raise HTTPException(
            status_code=400,  # noqa: WPS432
            detail="Invalid refresh token",
        )
    access_token = await create_access_token(user, "")
    new_refresh_token = await create_refresh_token(user, user_dao)
    return Tokens(  # noqa: S106
        access_token=access_token,
        refresh_token=new_refresh_token,
        token_type="Bearer",
        expires=settings.access_token_expire_minutes * 60,
    )
