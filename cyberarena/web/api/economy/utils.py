from datetime import datetime

from fastapi import Depends
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from cyberarena.db.dependencies import get_db_session
from cyberarena.db.models.user_model import UserModel
from cyberarena.settings import settings


def now() -> datetime:
    """
    Get current datetime.

    :return: current datetime.
    """
    return datetime.now()


async def _credit_account(
    user: UserModel,
    amount: int,
    reason: str,
) -> None:
    """
    Credit account to a valid user.

    Add amount specified to the user account.
    Warning: This function does not check if the user is valid.
    Warning: This function does not update the database.

    :param user: user to credit.
    :param amount: amount to credit.
    :param reason: reason for the credit.
    """
    if user.coins is None:
        user.coins = 0
        logger.warning(
            "User {user} has no coins, set to 0",
            user=user.username,
        )
    user.coins += amount
    logger.info(
        "User {user} credited with {amount} coins for : {reason}",
        user=user.username,
        amount=amount,
        reason=reason,
    )


async def _debit_account(
    user: UserModel,
    amount: int,
    reason: str,
) -> None:
    """
    Debit account to a valid user.

    Warning: This function does not check if the user is valid.
    Warning: This function does not check if the user has enough coins.
    Warning: This function does not update the database.

    :param user: user to debit.
    :param amount: amount to debit.
    :param reason: reason for the debit.
    """
    if user.coins is None:
        user.coins = 0
        logger.warning(
            "User {user} has no coins, set to 0",
            user=user.username,
        )
    user.coins -= amount
    if user.coins < 0:
        logger.warning(
            "User {user} has not enough coins to "
            "debit {amount} (created {amount_create}) coins for : {reason}",
            user=user.username,
            amount=amount,
            reason=reason,
            amount_create=user.coins,
        )
        user.coins = 0

    logger.info(
        "User {user} debited with {amount} coins for : {reason}",
        user=user.username,
        amount=amount,
        reason=reason,
    )


async def give_daily_free_coins(
    user: UserModel,
    session: AsyncSession = Depends(get_db_session),
) -> int:
    """
    Give daily free coins to a valid user.

    Chek if user has already claimed the daily free coins.
    Warning: This function does not check if the user is valid.

    :param user: user to give daily free coins.
    :param session: database session.
    :return: amount of coins given.
    """
    if (  # noqa: WPS337
        user.last_daily_reward is not None
        and user.last_daily_reward.date() >= now().date()
    ):
        return 0
    user.last_daily_reward = now()
    await _credit_account(user, settings.daily_coin_reward, "Daily free coins")
    await session.commit()
    return settings.daily_coin_reward
