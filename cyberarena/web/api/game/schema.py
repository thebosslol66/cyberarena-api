from typing import Optional

from pydantic import BaseModel

from cyberarena import game_module
from cyberarena.web.api.game.enums import TicketStatus


class TicketModel(BaseModel):
    """Ticket Model."""

    id: int
    status: TicketStatus
    room_id: Optional[int] = None
    player_id: Optional[int] = None


class CardModel(BaseModel):
    """Card Model."""

    id: int
    name: str
    description: str
    cost: Optional[int] = None
    damage: Optional[int] = None
    health: Optional[int] = None
    defense: Optional[int] = None
    rarity: game_module.enums.ObjectCardRarity
