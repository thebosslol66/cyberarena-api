from pydantic import BaseModel


class ChangeUserInformations(BaseModel):
    """Data for change password."""

    password: str
    new_setting: str
