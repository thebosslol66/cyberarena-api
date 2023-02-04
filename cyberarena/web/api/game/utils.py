from typing import Dict, List, Optional

from fastapi import HTTPException
from loguru import logger
from starlette import status
from starlette.websockets import WebSocket, WebSocketDisconnect

from cyberarena import game_module as gamem
from cyberarena.web.api.game.enums import TicketStatus
from cyberarena.web.api.game.schema import CardModel


class YourDaroneNotImplemented(NotImplementedError):
    """An error raised by your darone when don't make your homework or your methods."""


##############################################################################
#                    Ticket system for the game manager                      #
##############################################################################


class Ticket(object):
    """Ticket object."""

    def __init__(self, ticket_id: int, user_id: int) -> None:
        """
        Create a ticket.

        :param ticket_id: The id of the new ticket
        :param user_id: the user attached to the ticket
        """
        self.status: TicketStatus = TicketStatus.OPEN
        self.ticket_id = ticket_id
        self.user_id = user_id

    def __eq__(self, other: object) -> bool:
        """
        Compare ticket id.

        :param other: Another ticket or a ticket id
        :return: True if the ticket id are the same, False otherwise
        """
        if isinstance(other, int):
            return self.ticket_id == other
        if isinstance(other, Ticket):
            return self.ticket_id == other.ticket_id
        return False


class TicketManager(object):
    """Ticket manager."""

    def __init__(self) -> None:
        """Create a ticket manager."""
        self.__tickets: Dict[int, Ticket] = {}
        self.__history: Dict[int, Ticket] = {}

    def __len__(self) -> int:
        """
        Get the number of active tickets.

        :return: The number of active tickets
        """
        return len(self.__tickets)

    def ticket_active(self, ticket_id: int) -> bool:
        """
        Check if a ticket is active.

        :param ticket_id: The id of the ticket to check
        :return: True if the ticket is active, False otherwise
        """
        return ticket_id in self.__tickets.keys()

    def create_ticket(self, user_id: int) -> Ticket:
        """
        Create a ticket.

        :param user_id: The id of the user to attach to the ticket
        :return: The created ticket
        """
        ticket_id = len(self.__tickets) + len(self.__history)
        ticket = Ticket(ticket_id, user_id)
        self.__tickets[ticket_id] = ticket
        return ticket

    def get_ticket(self, ticket_id: int) -> Optional[Ticket]:
        """
        Get a ticket.

        It can be an active ticket or an archived one.

        :param ticket_id: The id of the ticket to get
        :return: The ticket or None if it doesn't exist
        """
        if ticket_id in self.__tickets.keys():
            return self.__tickets[ticket_id]
        if ticket_id in self.__history.keys():
            return self.__history[ticket_id]
        return None

    def has_open_ticket(self, user_id: int) -> bool:
        """
        Check if a user has an open ticket.

        :param user_id: The id of the user to check
        :return: True if the user has an open ticket, False otherwise
        """
        return self.get_ticket_by_user_id(user_id) is not None

    def get_ticket_by_user_id(self, user_id: int) -> Optional[Ticket]:
        """
        Get the ticket of a user.

        :param user_id: The id of the user to get the ticket
        :return: The ticket or None if the user doesn't have an open ticket
        """
        for ticket in self.__tickets.values():
            if ticket.user_id == user_id:
                return ticket
        return None

    def get_ticket_status(self, ticket_id: int) -> TicketStatus:
        """
        Get the status of a ticket.

        :param ticket_id: The id of the ticket to get the status
        :return: The status of the ticket
        """
        if ticket_id in self.__tickets:
            return TicketStatus.OPEN
        for ticket in self.__history.values():
            if ticket.ticket_id == ticket_id:
                return ticket.status
        return TicketStatus.DONT_EXIST

    def cancel_ticket(self, ticket_id: int) -> Optional[Ticket]:
        """
        Cancel an active ticket.

        :param ticket_id: The id of the ticket to cancel
        :return: The canceled ticket or None if the ticket doesn't exist
        """
        if ticket_id not in self.__tickets.keys():
            return None
        ticket = self.__tickets[ticket_id]
        ticket.status = TicketStatus.CANCEL
        self.__history[ticket_id] = ticket
        self.__tickets.pop(ticket_id)
        return ticket

    def close_ticket(self, ticket_id: int) -> Optional[Ticket]:
        """
        Close an active ticket.

        :param ticket_id: The id of the ticket to close
        :return: The closed ticket or None if the ticket doesn't exist
        """
        if ticket_id not in self.__tickets.keys():
            return None
        ticket = self.__tickets[ticket_id]
        ticket.status = TicketStatus.CLOSED
        self.__history[ticket_id] = ticket
        self.__tickets.pop(ticket_id)
        return ticket

    def find_match(self) -> None:
        """Find a match."""
        while len(self.__tickets) > 1:
            ticket1 = self.__tickets.popitem()
            ticket2 = self.__tickets.popitem()
            ticket1[1].status = TicketStatus.CLOSED
            ticket2[1].status = TicketStatus.CLOSED
            self.__history[ticket1[0]] = ticket1[1]
            self.__history[ticket2[0]] = ticket2[1]
            gamem.game_manager.create_game(
                ticket1[1].user_id,
                ticket2[1].user_id,
                gamem.create_deck(),
                gamem.create_deck(),
            )


ticket_manager = TicketManager()


##############################################################################
#                     Card related functions and classes                     #
##############################################################################
def get_card_data(card_id: int) -> CardModel:
    """
    Get a CardModel from a card id.

    :param card_id: The id of the card to get  # noqa: DAR003
    :return: The CardModel of the card
    :raises HTTPException: If the card doesn't exist
    """
    try:
        card = gamem.get_card_from_id(card_id)
        if isinstance(card, gamem.AbstractCharacterCard):
            return CardModel(
                id=card_id,
                name=card.name,
                description=card.description,
                cost=card.cost,
                attack=card.ap,
                defense=card.dp,
                health=card.hp,
                rarity=card.rarity,
            )
        return CardModel(
            id=card_id,
            name=card.name,
            description=card.description,
            cost=card.cost,
            rarity=card.rarity,
        )

    except gamem.exceptions.LibraryCardNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Card not found",
        )


def get_card_path(card_id: int, full_path: bool = False) -> str:
    """
    Get the path of a card.

    :param card_id: The id of the card to get the path.
    :param full_path: If True, get the image with stat filled.
    :return: The path of the card
    """
    return gamem.get_path_card_image(card_id, full_path)


class WebsocketGameManager(object):
    """Manage the websocket of the game."""

    def __init__(self) -> None:
        """Initialize the WebsocketGameManager."""
        self.__websocket_games: Dict[int, List[WebSocket]] = {}
        self.__websocket_to_player: Dict[WebSocket, int] = {}

    async def connect(self, websocket: WebSocket, game_id: int, user_id: int) -> None:
        """
        Connect a websocket to a game.

        :param websocket: The websocket to connect
        :param game_id: The id of the game to connect
        :param user_id: The id of the user to connect
        :raises HTTPException: If the user is not in the game
        """
        try:
            if user_id not in gamem.game_manager[game_id]:
                await websocket.close()
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="User not in this game",
                )
        except gamem.exceptions.GameNotFoundError:
            await websocket.close()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Game not found",
            )
        if game_id not in self.__websocket_games.keys():
            self.__websocket_games[game_id] = []
        self.__websocket_games[game_id].append(websocket)
        self.__websocket_to_player[websocket] = user_id
        await websocket.accept()
        if gamem.game_manager.connect(game_id, user_id):
            await self.begin_game(game_id)

    async def disconnect(self, websocket: WebSocket, game_id: int) -> None:
        """
        Disconnect a websocket from a game.

        :param websocket: The websocket to disconnect
        :param game_id: The id of the game to disconnect
        """
        if game_id in self.__websocket_games.keys():
            if websocket in self.__websocket_games[game_id]:
                self.__websocket_games[game_id].remove(websocket)
                self.__websocket_to_player.pop(websocket)
            if not self.__websocket_games[game_id]:
                self.__websocket_games.pop(game_id)

    async def game_broadcast(self, game_id: int, data: Dict[str, str]) -> None:
        """
        Send a message to all players in a game.

        :param game_id: The id of the game
        :param data: The data to send
        """
        if game_id in self.__websocket_games:
            for websocket in self.__websocket_games[game_id]:
                try:
                    await websocket.send_json(data)
                except WebSocketDisconnect:
                    await self.disconnect(websocket, game_id)

    async def game_private_broadcast(
        self,
        game_id: int,
        data: Dict[str, str | Dict[str, str | int]],
        target: WebSocket,
        data_for_other: Dict[str, str],
    ) -> None:
        """
        Send a message to one player while sending another one to the other player.

        :param game_id: The id of the game
        :param data: The data to send to the target
        :param data_for_other: The data to send to the other players
        :param target: The target of the data
        """
        if game_id in self.__websocket_games:
            for websocket in self.__websocket_games[game_id]:
                try:
                    if websocket == target:
                        await websocket.send_json(data)
                    else:
                        await websocket.send_json(data_for_other)
                except WebSocketDisconnect:
                    await self.disconnect(websocket, game_id)

    async def receive(
        self,
        websocket: WebSocket,
        data: Dict[str, str],
        room_id: int,
        user_id: int,
    ) -> None:
        """
        Recieve messages from players' websockets.

        :param websocket: The websocket to recieve from
        :param data: The data to recieve
        :param room_id: The id of the room of the player
        :param user_id: The id of the player
        """
        if data["type"] == "play_card":
            await self.deploy_card(room_id, websocket, data)
        elif data["type"] == "draw_card":
            await self.draw_card(room_id, websocket)
        elif data["type"] == "end_turn":
            await self.next_turn(room_id, websocket)
        elif data["type"] == "attack":
            await self.attack(room_id, websocket, data)

    async def begin_game(self, game_id: int) -> None:
        """
        Begin the game.

        :param game_id: The id of the game to begin
        """
        await self.game_broadcast(game_id, {"type": "begin_game"})
        for _ in range(gamem.get_starting_cards_amount()):
            for websocket in self.__websocket_games[game_id]:
                await self.draw_card(game_id, websocket)

    async def set_websocket_turn(self, game_id: int) -> None:
        """
        Get the turn of the game.

        :param game_id: The id of the game
        """
        if game_id in self.__websocket_games:
            for websocket in self.__websocket_games[game_id]:
                try:
                    await websocket.send_json(
                        {
                            "type": "set_turn",
                            "is_turn": gamem.game_manager.get_turn(
                                game_id,
                            )
                            == self.__websocket_to_player[websocket],
                        },
                    )
                except WebSocketDisconnect:
                    await self.disconnect(websocket, game_id)

    async def draw_card(self, game_id: int, websocket: WebSocket) -> None:
        """
        Draw a card.

        :param game_id: The id of the game
        :param websocket: The socket of the user
        """
        user_id = self.__websocket_to_player[websocket]
        card = gamem.game_manager.draw_card(game_id, user_id)
        if card is None:
            logger.error("No card to draw")
            return
        await self.game_private_broadcast(
            game_id,
            {
                "type": "draw_card",
                "card": card.to_dict(),
            },
            websocket,
            {"type": "draw_card_private"},
        )

    async def next_turn(self, game_id: int, websocket: WebSocket) -> None:
        """
        End the turn.

        :param game_id: The id of the game
        :param websocket: The socket of the user
        :raises YourDaroneNotImplemented: Your darone is not implemented
        """
        # TODO: finir
        raise YourDaroneNotImplemented()

    async def deploy_card(
        self,
        game_id: int,
        websocket: WebSocket,
        data: Dict[str, str],
    ) -> None:
        """
        Deploy a card.

        :param game_id: The id of the game
        :param websocket: The socket of the user
        :param data: json with the card
        :raises YourDaroneNotImplemented: Your darone is not implemented
        """
        # TODO finir
        raise YourDaroneNotImplemented()

    async def attack(
        self,
        game_id: int,
        websocket: WebSocket,
        data: Dict[str, str],
    ) -> None:
        """
        Play a card.

        :param game_id: The id of the game
        :param websocket: The socket of the user
        :param data: json with both cards
        :raises YourDaroneNotImplemented: Your darone is not implemented
        """
        # TODO finir
        raise YourDaroneNotImplemented()


websocket_manager = WebsocketGameManager()
