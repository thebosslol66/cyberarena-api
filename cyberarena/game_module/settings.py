from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    deck_size: int = 20
    board_size: int = 5

    card_data_filename: str = "data.json"
    card_image_filename: str = "card.png"

    class Config:
        env_file = ".env"
        env_prefix = "GAME_MODULE_"
        env_file_encoding = "utf-8"


settings = Settings()
