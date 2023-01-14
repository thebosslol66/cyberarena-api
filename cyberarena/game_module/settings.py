from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    deck_size: int = 20

    class Config:
        env_file = ".env"
        env_prefix = "GAME_MODULE_"
        env_file_encoding = "utf-8"


settings = Settings()
