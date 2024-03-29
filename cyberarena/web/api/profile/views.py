import os
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from starlette.responses import FileResponse

from cyberarena.db.dao.user_dao import UserDAO
from cyberarena.db.models.user_model import UserModel
from cyberarena.settings import settings
from cyberarena.web.api.connection.utils import get_current_user
from cyberarena.web.api.profile.change import router as change_router
from cyberarena.web.api.profile.schema import UserInformations

router = APIRouter()
router.include_router(change_router)


@router.get(
    "/me",
    response_model=UserInformations,
    summary="Get user informations.",
    description="Get informations about current logged user.\n",
)
async def get_current_user_profile(
    current_user: UserModel = Depends(get_current_user),
) -> UserInformations:
    """
    Get current user profile.

    :param current_user: current user.
    :return: current user profile.
    """
    return UserInformations(
        username=current_user.username,
        email=current_user.email,
        active=current_user.is_active,
    )


# TODO: know if the profile is accessible by everyone or only connected user
# TODO: If the profile is acessible by everyone, select if all is
#  accessible by everyone or only connected user
@router.get(
    "/{username}",
    summary="Get informations of the user with username.",
    description="Get informations of the user with username.\n"
    "\nIf the user is not found, "
    "you will have a status code of 404.\n",
)
async def get_specified_user_profile(
    username: str,
    user_dao: UserDAO = Depends(),
) -> str:
    """
    Return informations about a specific user with his username.

    :param username: username of profile to get.
    :param user_dao: user_dao.
    :raises HTTPException: if the user is not found.
    :return: informations about the user.
    """
    user = await user_dao.get_user_by_username(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return username


@router.get(
    "/me/avatar",
    response_class=FileResponse,
    summary="Get user's avatar.",
    description="Get user's avatar wich is logged in. "
    "It return it's avatar file,\n"
    "\nIf the user has no avatar, return a default avatar.\n",
)
async def get_current_user_avatar(
    current_user: UserModel = Depends(get_current_user),
) -> FileResponse:
    """
    Get current user avatar.

    :param current_user: current user.
    :return: current user avatar.
    :raises HTTPException: if user is not logged.
    """
    if current_user.id is not None:
        file_path: str = os.path.join(
            settings.avatar_path,
            "{0}.png".format(current_user.id),
        )
        if os.path.exists(file_path):
            return FileResponse(
                file_path,
                media_type="image/png",
                filename="avatar.png",
            )
        # return a default image if user haven't an avatar
        default_id_img: int = (
            current_user.id
            % len(
                os.listdir(os.path.join(settings.avatar_path, "default")),
            )
            + 1
        )
        return FileResponse(
            os.path.join(
                settings.avatar_path,
                "default",
                "{0}.png".format(default_id_img),
            ),
            media_type="image/png",
            filename="avatar.png",
        )
    raise HTTPException(  # pragma: no cover
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Avatar not found",
    )


@router.get(
    "/{username}/avatar",
    response_class=FileResponse,
    summary="Get user's avatar.",
    description="Get user's avatar with his username. "
    "It return it's avatar file,\n"
    "\nIf the user has no avatar, return a default avatar.\n",
)
async def get_specified_user_avatar(
    username: str,
    user_dao: UserDAO = Depends(),
) -> FileResponse:
    """
    Get the avatar image of a user.

    It's a PNG image with maximum size of 512x512 pixels.

    :param username: username of the user.
    :param user_dao: user dao.
    :return: the avatar image of the user.
    :raises HTTPException: if the user does not exist.
    """
    user: Optional[UserModel] = await user_dao.get_user_by_username(username)
    if user is not None:
        file_path: str = os.path.join(settings.avatar_path, "{0}.png".format(user.id))
        if os.path.exists(file_path):
            return FileResponse(
                file_path,
                media_type="image/png",
                filename="avatar.png",
            )
        # return a default image if user haven't an avatar
        if user.id is not None:
            default_id_img: int = (
                user.id
                % len(
                    os.listdir(os.path.join(settings.avatar_path, "default")),
                )
                + 1
            )
            return FileResponse(
                os.path.join(
                    settings.avatar_path,
                    "default",
                    "{0}.png".format(default_id_img),
                ),
                media_type="image/png",
                filename="avatar.png",
            )
    raise HTTPException(  # pragma: no cover
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found",
    )
