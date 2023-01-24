from typing import List

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


class Tokens(BaseModel):
    """Tokens for user."""

    access_token: str
    refresh_token: str
    token_type: str
    expires: int


class TokenData(BaseModel):
    """Data for token."""

    user_id: int
    scopes: List[str] = []


class AskNewTokenData(BaseModel):
    """Data for ask new token."""

    refresh_token: str
