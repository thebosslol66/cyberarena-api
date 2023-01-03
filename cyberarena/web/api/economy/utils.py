from datetime import datetime

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

import logging
from loguru import logger

from cyberarena.db.dao.user_dao import UserDAO
from cyberarena.db.models.user_model import UserModel
from dependencies import get_db_session
from settings import settings


async def _credit_account(
    user: UserModel,
    amount: int,
    reason: str,
    session: AsyncSession = Depends(get_db_session)
) -> None:
    """
    Credit account to a valid user.
    Warning: This function does not check if the user is valid.
    Warning: This function does not update the database.

    :param user: user to credit.
    :param amount: amount to credit.
    :param reason: reason for the credit.
    :param session: database session.
    """
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
session: AsyncSession = Depends(get_db_session)
) -> None:
    """
    Debit account to a valid user.
    Warning: This function does not check if the user is valid.
    Warning: This function does not check if the user has enough coins.
    Warning: This function does not update the database.

    :param user: user to debit.
    :param amount: amount to debit.
    :param reason: reason for the debit.
    :param session: database session.
    """
    user.coins -= amount
    logger.info(
        "User {user} debited with {amount} coins for : {reason}",
        user=user.username,
        amount=amount,
        reason=reason,
    )



async def give_daily_free_coins(
    user: UserModel,
session: AsyncSession = Depends(get_db_session)
) -> None:
    """
    Give daily free coins to a valid user.
    Chek if user has already claimed the daily free coins.
    Warning: This function does not check if the user is valid.

    :param user: user to give daily free coins.
    :param session: database session.
    """
    if user.last_daily_reward.date() >= datetime.now().date():
        return
    user.last_daily_reward = datetime.now()
    await _credit_account(user, settings.daily_coin_reward, "Daily free coins")
    await session.commit()
