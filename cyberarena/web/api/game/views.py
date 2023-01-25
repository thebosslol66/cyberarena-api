import uuid

from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from starlette.responses import FileResponse

from cyberarena.db.models.user_model import UserModel
from cyberarena.web.api.connection.utils import get_current_user
from cyberarena.web.api.game.schema import CardModel, TicketModel, TicketStatus
from cyberarena.web.api.game.utils import ticket_manager

router = APIRouter()
ticket_router = APIRouter()
router.include_router(ticket_router, prefix="/ticket", tags=["ticket"])


@ticket_router.get("/open")
async def open_ticket(
    current_user: UserModel = Depends(get_current_user),
) -> TicketModel:
    """
    Open a ticket for the matchmaker.

    :param current_user: The current user
    :return: The ticket
    :raises HTTPException: If the user is not active or already has an open ticket
    """
    if not current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have to be logged in to open a ticket.",
        )
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have to be active to open a ticket.",
        )
    if ticket_manager.has_open_ticket(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already have an open ticket.",
        )
    # TODO: verify if in game
    ticket_manager.create_ticket(current_user.id)
    return TicketModel(
        id=uuid.uuid4(),
        status=TicketStatus.OPEN,
    )


@ticket_router.get("/cancel")
async def cancel_ticket(
    ticket_id: int,
    current_user: UserModel = Depends(get_current_user),
) -> TicketModel:
    """
    Cancel an open ticket.

    :param ticket_id: The id of the ticket to cancel
    :param current_user: The current user
    :return: The canceled ticket
    :raises HTTPException: If the ticket is not open
    """
    if not ticket_manager.ticket_active(ticket_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ticket is not cancellable.",
        )
    ticket_manager.cancel_ticket(ticket_id)
    return TicketModel(
        id=ticket_id,
        status=TicketStatus.CANCEL,
    )


@ticket_router.get("/status")
async def get_ticket_status(
    ticket_id: int,
    current_user: UserModel = Depends(get_current_user),
) -> TicketModel:
    """
    Get the status of a ticket.

    :param ticket_id: The id of the ticket to get the status
    :param current_user: The current user
    :return: The status of the ticket
    :raises HTTPException: If the ticket doesn't exist or is closed
    """
    ticket_manager.find_match()
    statu: TicketStatus = ticket_manager.get_ticket_status(ticket_id)
    if statu == TicketStatus.DONT_EXIST:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ticket doesn't exist.",
        )
    if statu == TicketStatus.CLOSED:
        # TODO: get room id from user id from game manager
        pass  # noqa: WPS420
    return TicketModel(
        id=ticket_id,
        status=statu,
    )


@router.get("/card/{card_id}/data")
async def get_card(card_id: int) -> CardModel:
    """
    Get a card.

    :param card_id: The id of the card to get
    :return: The card
    :raises HTTPException: If the card doesn't exist
    """
    card = CardModel(
        id=card_id,
        name="Card",
        description="Description",
        cost=1,
        damage=1,
        health=1,
        defense=1,
    )
    if card is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Card doesn't exist.",
        )
    return card


@router.get("/card/{card_id}/image")
async def get_card_image(card_id: int) -> FileResponse:
    """
    Get the image of a card.

    :param card_id: The id of the card to get the image
    :return: The image of the card
    """
    return FileResponse("cyberarena/tests_data/imgs/test_avatar_good_512x512.png")