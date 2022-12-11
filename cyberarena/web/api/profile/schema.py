from pydantic import BaseModel


class ChangePassword(BaseModel):
    """Data for change password."""

    old_password: str
    new_password: str


class ChangeEMail(BaseModel):
    """Data for change email."""

    password: str
    new_email: str
