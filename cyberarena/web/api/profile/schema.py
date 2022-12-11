from pydantic import BaseModel


class UserInformations(BaseModel):
    """Data for user informations."""

    username: str
    email: str
    active: bool
