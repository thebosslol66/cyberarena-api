from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from cyberarena.db.dao.user_dao import UserDAO
from cyberarena.db.models.user_model import UserModel
from cyberarena.web.api.connection.utils import (
    VerifyUserModel,
    get_current_user,
    is_password_correct,
)
from cyberarena.web.api.profile.change.schema import ChangeUserInformations

router: APIRouter = APIRouter(prefix="/change", tags=["change"])


@router.put("/password")
async def change_password(
    password_data: ChangeUserInformations,
    user: UserModel = Depends(get_current_user),
    user_dao: UserDAO = Depends(),
) -> None:
    """
    Change user password.

    :param password_data: data for change password.
    :param user: current user.
    :param user_dao: user dao.
    :raises HTTPException: if password is incorrect or new password is incorrect.
    """
    if user.is_correct_password(password_data.password):
        if password_data.new_setting == password_data.password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Passwords are the same",
            )

        user_model = VerifyUserModel("", password_data.new_setting, "", user_dao)

        if not is_password_correct(user_model):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The new password is not correct",
            )
        await user_dao.update_password(
            user.id if user.id is not None else -1,
            password_data.new_setting,
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wrong old password",
        )


@router.put("/email")
async def change_email(
    change_email_data: ChangeUserInformations,
    user: UserModel = Depends(get_current_user),
    user_dao: UserDAO = Depends(),
) -> None:
    """
    Change user email.

    :param change_email_data: data for change email.
    :param user: current user.
    :param user_dao: user dao.
    :raises HTTPException: if email is incorrect.
    """
    if user.is_correct_password(change_email_data.password):
        if user_dao.get_user_by_email(change_email_data.new_setting) is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already used",
            )
        await user_dao.update_email(
            user.id if user.id is not None else -1,
            change_email_data.new_setting,
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wrong password",
        )


@router.put("/username")
async def change_username(
    change_username_data: ChangeUserInformations,
    user: UserModel = Depends(get_current_user),
    user_dao: UserDAO = Depends(),
) -> None:
    """
    Change user username.

    :param change_username_data: data for change username.
    :param user: current user.
    :param user_dao: user dao.
    :raises HTTPException: if username is incorrect.
    """
    if user.is_correct_password(change_username_data.password):
        if user_dao.get_user_by_username(change_username_data.new_setting) is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already used",
            )
        await user_dao.update_username(
            user.id if user.id is not None else -1,
            change_username_data.new_setting,
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wrong password",
        )
