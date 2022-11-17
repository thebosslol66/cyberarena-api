from pydantic import BaseModel


class SignUpStatusDTO(BaseModel):
    """DTO for sign up status."""

    status: int
    message: str
