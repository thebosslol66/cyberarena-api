from fastapi import APIRouter, Depends

from cyberarena.db.models.user_model import UserModel
from cyberarena.web.api.connection.utils import get_current_user
from cyberarena.web.api.economy.utils import give_daily_free_coins

router = APIRouter()


@router.get("/daily-reward", response_model=int)
async def ask_daily_free_coins(
    user: UserModel = Depends(get_current_user),
) -> int:
    """
    Ask daily free coins to a valid user.

    Check if user has already claimed the daily free coins.
    Warning: This function does not check if the user is valid.

    :param user: user to give daily free coins.
    :return: amount of coins given.
    """
    return await give_daily_free_coins(user)
