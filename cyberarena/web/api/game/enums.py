import enum


class TicketStatus(str, enum.Enum):  # noqa: WPS600
    """Ticket status."""

    OPEN = "open"
    CLOSED = "closed"
    CANCEL = "cancel"
    DONT_EXIST = "dont_exist"
