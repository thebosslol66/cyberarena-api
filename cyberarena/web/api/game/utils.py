from enum import auto
from typing import Dict, Optional

from strenum import LowercaseStrEnum


class TicketStatus(LowercaseStrEnum):
    """Ticket status."""

    OPEN = auto()
    CLOSED = auto()
    CANCLED = auto()
    DONT_EXIST = auto()


class Ticket(object):
    """Ticket object."""

    def __init__(self, ticket_id: int, user_id: int) -> None:
        """
        Create a ticket.

        :param ticket_id: The id of the new ticket
        :param user_id: the user attached to the ticket
        """
        self.status: TicketStatus = TicketStatus.OPEN  # type: ignore[assignment]
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
            return TicketStatus.OPEN  # type: ignore[return-value]
        for ticket in self.__history.values():
            if ticket.ticket_id == ticket_id:
                return ticket.status
        return TicketStatus.DONT_EXIST  # type: ignore[return-value]

    def cancel_ticket(self, ticket_id: int) -> Optional[Ticket]:
        """
        Cancel an active ticket.

        :param ticket_id: The id of the ticket to cancel
        :return: The canceled ticket or None if the ticket doesn't exist
        """
        if ticket_id not in self.__tickets.keys():
            return None
        ticket = self.__tickets[ticket_id]
        ticket.status = TicketStatus.CANCLED  # type: ignore[assignment]
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
        ticket.status = TicketStatus.CLOSED  # type: ignore[assignment]
        self.__history[ticket_id] = ticket
        self.__tickets.pop(ticket_id)
        return ticket

    def find_match(self) -> None:
        """Find a match."""
        while len(self.__tickets) > 1:
            ticket1 = self.__tickets.popitem()
            ticket2 = self.__tickets.popitem()
            ticket1[1].status = TicketStatus.CLOSED  # type: ignore[assignment]
            ticket2[1].status = TicketStatus.CLOSED  # type: ignore[assignment]
            self.__history[ticket1[0]] = ticket1[1]
            self.__history[ticket2[0]] = ticket2[1]


ticket_manager = TicketManager()
