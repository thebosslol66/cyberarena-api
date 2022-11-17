from pydantic import BaseModel


class SignUpData(BaseModel):
    """Data for sign up a user."""

    username: str
    password: str
    email: str


class SignUpStatusDTO(BaseModel):
    """DTO for sign up status."""

    status: int
    message: str
