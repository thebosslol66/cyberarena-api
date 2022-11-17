from fastapi import APIRouter, Depends

from cyberarena.db.dao.user_dao import UserDAO
from cyberarena.web.api.connection.schema import SignUpStatusDTO
from cyberarena.web.api.connection.utils import verify_user_sign_in

router = APIRouter()


@router.post("/sign-up", response_model=SignUpStatusDTO)
async def sign_up(
    username: str,
    password: str,
    email: str,
    user_dao: UserDAO = Depends(),
) -> SignUpStatusDTO:
    """
    Sign up user.

    :param user_dao: DAO for user models.
    :param username: username of user.
    :param password: password of user.
    :param email: email of user.
    :return: status of sign up.
    """
    response = await verify_user_sign_in(username, password, email, user_dao)
    # Create user
    if response.status == 0:
        await user_dao.create_user(username, password, email)
        response.message = "User created"
    return response
