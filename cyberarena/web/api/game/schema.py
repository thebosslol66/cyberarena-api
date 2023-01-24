from typing import Optional

from pydantic import BaseModel

from cyberarena.web.api.game.utils import TicketStatus


class TicketModel(BaseModel):
    """Ticket Model."""

    id: int
    status: TicketStatus
    room_id: Optional[int] = None


class CardModel(BaseModel):
    """Card Model."""

    id: int
    name: str
    description: str
    cost: int
    damage: int
    health: int
    defense: int
