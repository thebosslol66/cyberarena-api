from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

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


@router.post(
    "/sign-up",
    response_model=SignUpStatusDTO,
    summary="Sign up new user.",
    description="Sign up new user with a username, an email and a password.\n"
    "\nThe email must be valid and a mail will"
    " be send to confirm it.\n\n"
    "If the user is register correctly"
    " you will have a status code of 0.\n"
    "\n* 1: The username is not correct\n"
    "* 2: The password is not correct\n"
    "* 3: The email is not correct\n"
    "* 4: The username is already used\n"
    "* 5: The email is already used\n"
    "\n The name must do 4 char minimum and only contain"
    "letters and numbers.\n"
    "\n The password must do 8 char minimum and contain at least "
    "one small letter, one capital letter and one number "
    "and one special character.\n",
)
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
        user: Optional[UserModel] = await user_dao.get_user_by_username(sign_up_data.username)
        if user is not None and user.id is not None:
            await user_dao.update_active(user.id, active=True)
        response.message = "User created"
    return response


@router.get(
    "/activate",
    summary="Activate user account.",
    description="Activate user account with the token send by email.\n",
)
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


@router.post(
    "/token",
    response_model=Tokens,
    summary="Get a token from login credentials.",
    description="Get a token from login credentials.\n"
    "\nIf the credentials are not correct return 400 http error "
    "with the description of error.\n\n"
    "For the moment, if the user is inactive, it return error 400 "
    "too.",
)
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
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
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


@router.post(
    "/refresh-token",
    response_model=Tokens,
    summary="Get a new access token with a refresh token.",
    description="Get a new access token with a refresh token.\n\n"
    "The refresh token must be valid and not expired.\n\n"
    "If the same refresh token is used twice, "
    "it invalid all refresh token.",
)
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
    if user is None:
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
