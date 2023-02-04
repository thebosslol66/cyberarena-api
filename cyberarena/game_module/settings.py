from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    starting_cards_in_deck: int = 3
    deck_size: int = 20
    board_size: int = 5

    card_path: str = "./cyberarena/data/cards"
    card_data_filename: str = "data.json"
    card_image_filename: str = "card.png"

    font_card_path: str = "./cyberarena/data/fonts/Valorax-lg25V.otf"
    font_big_size: int = 36
    font_normal_size: int = 20

    class Config:
        env_file = ".env"
        env_prefix = "GAME_MODULE_"
        env_file_encoding = "utf-8"


settings = Settings()
