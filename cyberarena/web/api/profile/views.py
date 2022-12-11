from fastapi import APIRouter, Depends

from cyberarena.db.models.user_model import UserModel
from cyberarena.web.api.connection.utils import get_current_user
from cyberarena.web.api.profile.change import router as change_router
from cyberarena.web.api.profile.schema import UserInformations

router = APIRouter()
router.include_router(change_router)


@router.get("/me", response_model=UserInformations)
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
