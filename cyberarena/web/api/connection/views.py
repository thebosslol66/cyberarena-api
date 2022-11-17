from fastapi import APIRouter, Depends

from cyberarena.db.dao.user_dao import UserDAO
from cyberarena.web.api.connection.schema import SignUpData, SignUpStatusDTO
from cyberarena.web.api.connection.utils import verify_user_sign_in

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
    return response
