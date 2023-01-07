from fastapi import APIRouter, Depends, HTTPException, UploadFile
from PIL import Image
from starlette import status

from cyberarena.db.dao.user_dao import UserDAO
from cyberarena.db.models.user_model import UserModel
from cyberarena.settings import settings
from cyberarena.web.api.connection.utils import (
    VerifyUserModel,
    get_current_user,
    is_email_correct,
    is_password_correct,
)
from cyberarena.web.api.profile.change.schema import ChangeUserInformations

router: APIRouter = APIRouter(prefix="/change")


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

        if (await is_password_correct(user_model)) is not None:
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
        second_user = await user_dao.get_user_by_email(change_email_data.new_setting)
        if second_user is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already used",
            )
        user_model = VerifyUserModel("", "", change_email_data.new_setting, user_dao)
        if (await is_email_correct(user_model)) is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The new email is not correct",
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
        second_user = await user_dao.get_user_by_username(
            change_username_data.new_setting,
        )
        if second_user is not None:
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


async def save_avatar_img(avatar_img: UploadFile, path: str) -> dict[str, str]:
    """
    Save the avatar image to the static/img/avatars folder.

    :param avatar_img: avatar image.
    :param path: path to save the image including it's name.
    :return: dict with the key msg to tell the image has been saved.
    :raises HTTPException: if the image failed to be saved.
    """
    try:
        # Open the img as same as the original image
        img = Image.open(avatar_img.file)
        img.save(path, "PNG", optimize=True)
        return {"msg": "Avatar changed"}

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="The image cannot be saved",
        )


@router.put("/avatar")
async def change_avatar(
    avatar_img: UploadFile,
    user: UserModel = Depends(get_current_user),
) -> dict[str, str]:
    """
    Change the user avatar with the new pass in parameters.

    Maximum size of the image is 1MB and must do at maximum 512x512 pixels
    Must verify that the image is a png or jpg and not contain any
    malicious code or software

    :param avatar_img: the new avatar image.
    :param user: current user.
    :return: if the avatar image has been updated.
    :raises HTTPException: if the image is not a png or jpg or if the image is too big
    """
    error: str = ""
    if avatar_img.content_type not in {"image/png", "image/jpeg"}:
        error = "The image must be a png or jpg"

    avatar_img.file.seek(0, 2)
    if avatar_img.file.tell() > settings.max_avatar_size:
        error = "The image is too big"
    avatar_img.file.seek(0, 0)

    if user.id is None:
        error = "User not found"

    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error,
        )

    path: str = f"cyberarena/static/img/avatars/{user.id}.png"
    return await save_avatar_img(avatar_img, path)
