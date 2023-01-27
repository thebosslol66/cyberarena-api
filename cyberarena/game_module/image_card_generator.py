# pragma: no cover
# flake8: noqa
import logging
import os
from typing import List, Tuple, Union

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from cyberarena.game_module.card.base import AbstractCard, AbstractCharacterCard
from cyberarena.game_module.card.enums import ObjectCardRace, ObjectCardRarity
from cyberarena.game_module.settings import settings

logger = logging.getLogger("cyberarena.game_module.image_generator")


def get_text_list_fit_width(
    text: Union[str, List[str]],
    width: int,
    font: ImageFont.ImageFont,
) -> List[str]:
    """
    Get a list of text that fit the width.

    Each element of the list is a line of text that fit the width.

    :param text: The text to split.
    :param font: The font used to draw the text.
    :param width: The width of the text.
    :return: A list of text that fit the width.
    """
    text_list = []
    if isinstance(text, list):
        for i, line in enumerate(text):
            text_list.extend(get_text_list_fit_width(line, width, font))
        return text_list
    text = text.split("\n")
    if len(text) > 1:
        return get_text_list_fit_width(text, width, font)
    text = text[0]
    text_list.append("")
    for word in text.split(" "):
        if font.getsize(text_list[-1] + " " + word)[0] <= width:
            text_list[-1] += " " + word
        else:
            text_list.append(word)
    return text_list


def is_data_or_image_newer_than_builded_card(
    data_filename: str,
    image_filename: str,
    builded_card_filename: str,
) -> bool:
    """
    Check if the data or the image is newer than the builded card.

    :param data_filename: The data filename.
    :param image_filename: The image filename.
    :param builded_card_filename: The builded card filename.
    :return: True if the data or the image is newer than the builded card, False otherwise.
    :raises FileNotFoundError: If the data or the image file is not found.
    """
    if not os.path.exists(builded_card_filename):
        logger.debug(
            f"The builded card '{builded_card_filename}' does not exist. "
            "The card will be builded.",
        )
        return True
    try:
        data_time = os.path.getmtime(data_filename)
        image_time = os.path.getmtime(image_filename)
        builded_card_time = os.path.getmtime(builded_card_filename)
    except FileNotFoundError as error:
        logger.error(error)
        raise error
    logger.debug(
        f"Data time: {data_time}, image time: {image_time}, "
        f"builded card time: {builded_card_time}"
        "\n"
        f"Data path: {data_filename}, image path: {image_filename}, "
        f"builded card path: {builded_card_filename}",
    )
    return data_time > builded_card_time or image_time > builded_card_time


class ImageCardGeneratorResources(object):
    """
    ImageCardGeneratorResources class.

    It contains all ressources used by all images to save memory.
    """

    HUMAN_COLORS = ((218, 171, 102), (250, 119, 254))  # Beige and pink
    ROBOT_COLORS = ((54, 137, 158), (47, 44, 41))  # Blue and grey
    ALIEN_COLORS = ((29, 229, 2), (35, 207, 203))  # Green and cyan
    MUTANT_COLORS = ((67, 22, 246), (146, 93, 215))  # Purple and violet

    COLORS_BY_RACE = {
        ObjectCardRace.HUMAN: HUMAN_COLORS,
        ObjectCardRace.ROBOT: ROBOT_COLORS,
        ObjectCardRace.ALIEN: ALIEN_COLORS,
        ObjectCardRace.MUTANT: MUTANT_COLORS,
    }

    WIDTH = 734
    HEIGHT = 1024
    RADIUS_CORNER = 50

    MAIN_IMAGE_WIDTH = 640
    MAIN_IMAGE_HEIGHT = 320

    MAIN_IMAGE_POSITION_X = int((WIDTH - MAIN_IMAGE_WIDTH) / 2)
    MAIN_IMAGE_POSITION_Y = 130
    MAIN_IMAGE_RADIUS_CORNER = 45

    NAME_WIDTH = MAIN_IMAGE_WIDTH
    NAME_HEIGHT = 70
    NAME_POSITION_X = int((WIDTH - MAIN_IMAGE_WIDTH) / 2)
    NAME_POSITION_Y = 20

    TEXT_COLOR = (255, 255, 255)
    TEXT_STROKE_COLOR = (0, 0, 0)
    TEXT_BIG_SIZE = settings.font_big_size
    TEXT_NORMAL_SIZE = settings.font_normal_size

    STATS_WIDTH = MAIN_IMAGE_WIDTH
    STATS_HEIGHT = 160
    STATS_POSITION = (
        int((WIDTH - MAIN_IMAGE_WIDTH) / 2),
        MAIN_IMAGE_POSITION_Y + MAIN_IMAGE_HEIGHT + 50,
    )

    STAT_HEALTH_POSITION = (30, 30)
    STAT_ATTACK_POSITION = (100, 30)
    STAT_DEFENSE_POSITION = (200, 30)
    STAT_DIVIDER_HORIZONTAL_SHIFT = 20
    STAT_DIVIDER_VERTICAL_SHIFT = 35
    STAT_STROKE_WIDTH = 8

    BASE_CARD_SHAPE = Image.new(
        "RGBA",
        (WIDTH, HEIGHT),
        (255, 255, 255, 0),
    )

    MAIN_IMAGE_MASK = Image.new(
        "RGBA",
        (MAIN_IMAGE_WIDTH, MAIN_IMAGE_HEIGHT),
        (255, 255, 255, 0),
    )

    NAME_BACKGROUND = Image.new(
        "RGBA",
        (NAME_WIDTH, NAME_HEIGHT),
        (255, 255, 255, 0),
    )

    FONT_PATH = settings.font_card_path

    BIG_TEXT_FONT = ImageFont.truetype(FONT_PATH, TEXT_BIG_SIZE)
    MEDIUM_TEXT_FONT = ImageFont.truetype(FONT_PATH, TEXT_NORMAL_SIZE)

    DESCRIPTION_POSITION = (
        int((WIDTH - MAIN_IMAGE_WIDTH) / 2),
        MAIN_IMAGE_POSITION_Y + MAIN_IMAGE_HEIGHT + 50 + STATS_HEIGHT + 50,
    )

    DESCRIPTION_WIDTH = MAIN_IMAGE_WIDTH
    DESCRIPTION_HEIGHT = 230
    DESCRIPTION_BACKGROUND = Image.new(
        "RGBA",
        (DESCRIPTION_WIDTH, DESCRIPTION_HEIGHT),
        (255, 255, 255, 0),
    )
    DESCRIPTION_PADDING = 25

    RARITY_SYMBOL_SIZE = 50
    RARITY_SYMBOL_BORDER_WIDTH = 2
    RARITY_SYMBOL_BORDER_COLOR = (0, 0, 0)
    RARITY_SYMBOL_POSITION = (
        WIDTH - int((WIDTH - MAIN_IMAGE_WIDTH) / 2) - RARITY_SYMBOL_SIZE,
        HEIGHT - RARITY_SYMBOL_SIZE - 20,
    )

    RARITY_SYMBOL_GOLD_HEXAGON = Image.new(
        "RGBA",
        (RARITY_SYMBOL_SIZE, RARITY_SYMBOL_SIZE),
        (255, 255, 255, 0),
    )
    RARITY_SYMBOL_VIOLET_SQUARE = Image.new(
        "RGBA",
        (RARITY_SYMBOL_SIZE, RARITY_SYMBOL_SIZE),
        (255, 255, 255, 0),
    )
    RARITY_SYMBOL_GREEN_TRIANGLE = Image.new(
        "RGBA",
        (RARITY_SYMBOL_SIZE, RARITY_SYMBOL_SIZE),
        (255, 255, 255, 0),
    )
    RARITY_SYMBOL_GREY_CIRCLE = Image.new(
        "RGBA",
        (RARITY_SYMBOL_SIZE, RARITY_SYMBOL_SIZE),
        (255, 255, 255, 0),
    )

    SYMBOL_BY_RARITY = {
        ObjectCardRarity.COMMON: RARITY_SYMBOL_GREY_CIRCLE,
        ObjectCardRarity.RARE: RARITY_SYMBOL_GREEN_TRIANGLE,
        ObjectCardRarity.EPIC: RARITY_SYMBOL_VIOLET_SQUARE,
        ObjectCardRarity.LEGENDARY: RARITY_SYMBOL_GOLD_HEXAGON,
    }

    def __init__(self) -> None:
        """Init the ImageCardGeneratorResources class."""
        self._output_folder: str = ""
        image_base_rounded_corners_draw = ImageDraw.Draw(
            self.BASE_CARD_SHAPE,
        )
        image_base_rounded_corners_draw.rounded_rectangle(
            (0, 0, self.WIDTH, self.HEIGHT),
            self.RADIUS_CORNER,
            fill=(255, 255, 255, 255),
        )

        image_main_base_rounded_corners_draw = ImageDraw.Draw(
            self.MAIN_IMAGE_MASK,
        )
        image_main_base_rounded_corners_draw.rounded_rectangle(
            (
                0,
                0,
                self.MAIN_IMAGE_WIDTH,
                self.MAIN_IMAGE_HEIGHT,
            ),
            self.MAIN_IMAGE_RADIUS_CORNER,
            fill=(255, 255, 255, 255),
        )

        background_text_encart_draw = ImageDraw.Draw(
            self.NAME_BACKGROUND,
        )
        background_text_encart_draw.rounded_rectangle(
            (0, 0, self.NAME_WIDTH, self.NAME_HEIGHT),
            self.MAIN_IMAGE_RADIUS_CORNER,
            fill=(0, 0, 0, 5),
        )

        background_description_encart_draw = ImageDraw.Draw(
            self.DESCRIPTION_BACKGROUND,
        )
        background_description_encart_draw.rounded_rectangle(
            (0, 0, self.DESCRIPTION_WIDTH, self.DESCRIPTION_HEIGHT),
            self.MAIN_IMAGE_RADIUS_CORNER,
            fill=(0, 0, 0, 50),
        )

        self.STATS_BACKGROUND = ImageCardGeneratorResources.generate_stats_background()

        # Draw the rarity symbols
        draw = ImageDraw.Draw(self.RARITY_SYMBOL_GOLD_HEXAGON)
        draw.polygon(
            (
                (self.RARITY_SYMBOL_SIZE / 2, 0),
                (self.RARITY_SYMBOL_SIZE, self.RARITY_SYMBOL_SIZE / 4),
                (self.RARITY_SYMBOL_SIZE, self.RARITY_SYMBOL_SIZE * 3 / 4),
                (self.RARITY_SYMBOL_SIZE / 2, self.RARITY_SYMBOL_SIZE),
                (0, self.RARITY_SYMBOL_SIZE * 3 / 4),
                (0, self.RARITY_SYMBOL_SIZE / 4),
            ),
            fill=(255, 168, 18, 255),
        )
        draw.polygon(
            (
                (self.RARITY_SYMBOL_SIZE / 2, 0),
                (self.RARITY_SYMBOL_SIZE, self.RARITY_SYMBOL_SIZE / 4),
                (self.RARITY_SYMBOL_SIZE, self.RARITY_SYMBOL_SIZE * 3 / 4),
                (self.RARITY_SYMBOL_SIZE / 2, self.RARITY_SYMBOL_SIZE),
                (0, self.RARITY_SYMBOL_SIZE * 3 / 4),
                (0, self.RARITY_SYMBOL_SIZE / 4),
            ),
            outline=self.RARITY_SYMBOL_BORDER_COLOR,
            width=self.RARITY_SYMBOL_BORDER_WIDTH,
        )

        draw = ImageDraw.Draw(self.RARITY_SYMBOL_VIOLET_SQUARE)
        draw.rectangle(
            (0, 0, self.RARITY_SYMBOL_SIZE, self.RARITY_SYMBOL_SIZE),
            fill=(138, 43, 226, 255),
        )
        draw.rectangle(
            (
                self.RARITY_SYMBOL_BORDER_WIDTH / 2,
                self.RARITY_SYMBOL_BORDER_WIDTH / 2,
                self.RARITY_SYMBOL_SIZE - self.RARITY_SYMBOL_BORDER_WIDTH / 2,
                self.RARITY_SYMBOL_SIZE - self.RARITY_SYMBOL_BORDER_WIDTH / 2,
            ),
            outline=self.RARITY_SYMBOL_BORDER_COLOR,
            width=self.RARITY_SYMBOL_BORDER_WIDTH,
        )

        draw = ImageDraw.Draw(self.RARITY_SYMBOL_GREEN_TRIANGLE)
        draw.polygon(
            [
                (0, self.RARITY_SYMBOL_SIZE),
                (self.RARITY_SYMBOL_SIZE, self.RARITY_SYMBOL_SIZE),
                (self.RARITY_SYMBOL_SIZE, 0),
            ],
            fill=(0, 128, 0, 255),
        )
        draw.polygon(
            [
                (
                    self.RARITY_SYMBOL_BORDER_WIDTH / 2,
                    self.RARITY_SYMBOL_SIZE - self.RARITY_SYMBOL_BORDER_WIDTH / 2,
                ),
                (
                    self.RARITY_SYMBOL_SIZE - self.RARITY_SYMBOL_BORDER_WIDTH / 2,
                    self.RARITY_SYMBOL_SIZE - self.RARITY_SYMBOL_BORDER_WIDTH / 2,
                ),
                (
                    self.RARITY_SYMBOL_SIZE - self.RARITY_SYMBOL_BORDER_WIDTH / 2,
                    self.RARITY_SYMBOL_BORDER_WIDTH / 2,
                ),
            ],
            outline=self.RARITY_SYMBOL_BORDER_COLOR,
            width=self.RARITY_SYMBOL_BORDER_WIDTH,
        )

        draw = ImageDraw.Draw(self.RARITY_SYMBOL_GREY_CIRCLE)
        draw.ellipse(
            (0, 0, self.RARITY_SYMBOL_SIZE, self.RARITY_SYMBOL_SIZE),
            fill=(128, 128, 128, 255),
        )
        draw.ellipse(
            (
                self.RARITY_SYMBOL_BORDER_WIDTH / 2,
                self.RARITY_SYMBOL_BORDER_WIDTH / 2,
                self.RARITY_SYMBOL_SIZE - self.RARITY_SYMBOL_BORDER_WIDTH / 2,
                self.RARITY_SYMBOL_SIZE - self.RARITY_SYMBOL_BORDER_WIDTH / 2,
            ),
            outline=self.RARITY_SYMBOL_BORDER_COLOR,
            width=self.RARITY_SYMBOL_BORDER_WIDTH,
        )

    @property
    def output_folder(self) -> str:
        """
        Get the output folder.

        :return: The output folder.
        """
        return self._output_folder

    @output_folder.setter
    def output_folder(self, output_folder: str) -> None:
        """
        Set the output folder.

        The output folder must exist.

        :param output_folder: The output folder.
        :raise ValueError: If the output folder does not exist.
        """
        if not os.path.exists(output_folder):
            raise ValueError("The output folder does not exist.")

        self._output_folder = output_folder

    @classmethod
    def generate_stats_background(cls) -> Image.Image:
        """
        Generate the image with the stats of the card.

        The stats image must be like this:
            +------------------------+
          HEALTH  /  DEFENSE  /  ATTACK
            1    /     1     /    1
        +------------------------+

        :return: The image with the stats of the card.
        """

        # Create the base image
        stats_image = Image.new(
            "RGBA",
            (cls.STATS_WIDTH, cls.STATS_HEIGHT),
            (255, 255, 255, 0),
        )
        draw = ImageDraw.Draw(stats_image)

        # Draw the horizontal lines
        draw.line(
            [
                (int(cls.STATS_WIDTH * 0.2), cls.STAT_STROKE_WIDTH / 2),
                (int(cls.STATS_WIDTH * 0.9), cls.STAT_STROKE_WIDTH / 2),
            ],
            fill=(0, 0, 0),
            width=cls.STAT_STROKE_WIDTH,
        )
        draw.line(
            [
                (
                    int(cls.STATS_WIDTH * 0.1),
                    cls.STATS_HEIGHT - cls.STAT_STROKE_WIDTH / 2,
                ),
                (
                    int(cls.STATS_WIDTH * 0.8),
                    cls.STATS_HEIGHT - cls.STAT_STROKE_WIDTH / 2,
                ),
            ],
            fill=(0, 0, 0),
            width=cls.STAT_STROKE_WIDTH,
        )

        # Draw diagonal divider lines
        draw.line(
            [
                (
                    int(cls.STATS_WIDTH * 0.33) + cls.STAT_DIVIDER_HORIZONTAL_SHIFT,
                    cls.STAT_DIVIDER_VERTICAL_SHIFT,
                ),
                (
                    int(cls.STATS_WIDTH * 0.33) - cls.STAT_DIVIDER_HORIZONTAL_SHIFT,
                    cls.STATS_HEIGHT - cls.STAT_DIVIDER_VERTICAL_SHIFT,
                ),
            ],
            fill=(0, 0, 0),
            width=cls.STAT_STROKE_WIDTH,
        )
        draw.line(
            [
                (
                    int(cls.STATS_WIDTH * 0.66) + cls.STAT_DIVIDER_HORIZONTAL_SHIFT,
                    cls.STAT_DIVIDER_VERTICAL_SHIFT,
                ),
                (
                    int(cls.STATS_WIDTH * 0.66) - cls.STAT_DIVIDER_HORIZONTAL_SHIFT,
                    cls.STATS_HEIGHT - cls.STAT_DIVIDER_VERTICAL_SHIFT,
                ),
            ],
            fill=(0, 0, 0),
            width=cls.STAT_STROKE_WIDTH,
        )

        stats_image.filter(ImageFilter.GaussianBlur(radius=1000))
        # Draw the text
        font = cls.BIG_TEXT_FONT
        _, _, w, h = draw.textbbox((0, 0), "HP", font=font)
        draw.text(
            (
                int(cls.STATS_WIDTH * 0.16) - w / 2,
                int(cls.STATS_HEIGHT * 0.3) - h / 2,
            ),
            "HP",
            font=font,
            fill=cls.TEXT_COLOR,
            stroke_width=2,
            stroke_fill=cls.TEXT_STROKE_COLOR,
        )
        _, _, w, h = draw.textbbox((0, 0), "DP", font=font)
        draw.text(
            (int(cls.STATS_WIDTH * 0.5) - w / 2, int(cls.STATS_HEIGHT * 0.3) - h / 2),
            "DP",
            font=font,
            fill=cls.TEXT_COLOR,
            stroke_width=2,
            stroke_fill=cls.TEXT_STROKE_COLOR,
        )
        _, _, w, h = draw.textbbox((0, 0), "AP", font=font)
        draw.text(
            (
                int(cls.STATS_WIDTH * 0.83) - w / 2,
                int(cls.STATS_HEIGHT * 0.3) - h / 2,
            ),
            "AP",
            font=font,
            fill=cls.TEXT_COLOR,
            stroke_width=2,
            stroke_fill=cls.TEXT_STROKE_COLOR,
        )

        return stats_image


class ImageCardGenerator(object):
    resources = ImageCardGeneratorResources()

    def __init__(self, card: AbstractCard, image_path: str) -> None:
        """
        Constructor.

        :param card: The card with all data to build the image.
        :param image_path: The path to the image of the card.
        """

        self._card: AbstractCard = card
        self._card_img: Image = Image.open(image_path)

        (self._image, self._image_draw) = self._generate_base_image()

    def generate_card(self) -> Image.Image:
        """
        Generate the card image for a given card.

        :return: The image of the card fully build.
        """
        self._place_main_image()
        self._place_card_name()
        if isinstance(self._card, AbstractCharacterCard):
            self._place_stats()
        self._place_card_description()
        self._place_card_rarity()
        return self._image

    def save_image(self, filename: str) -> None:
        """
        Seve the previously generated image into the directory with the filename.

        The directory mus be configure like this:
            ImageCardGenerator.resources.output_folder = output
        Then all files will be name with the filename and saved in the output folder.

        :param filename: The name of the file to save the image.
        """
        if not self._image:
            logger.error(
                "The image is not generated yet and will not be saved."
                "\nPlease call the generate_card() "
                "method before saving the image.",
            )
            return
        path = os.path.join(ImageCardGenerator.resources.output_folder, filename)
        self._image.save(path)
        logger.info(f"Image saved at {path}")

    def _generate_base_image(self) -> Tuple[Image.Image, ImageDraw.ImageDraw]:
        """
        Create the base image of the card.

        It create the background image (mostly a gradient)
        depending on the type of the card.
        It add o border to the card and a shadow.
        It prepare the card with some effects.
        More over it round the corners of the card.
        """
        # Create the background image of the card depending on the type of the card
        image = self.resources.BASE_CARD_SHAPE.copy()
        image_draw = ImageDraw.Draw(image)
        # Generate the gradient background depending on the type of the card
        gradient = self._generate_gradient()
        # Blend the gradient image with the base image
        image = Image.composite(gradient, image, image)
        return image, image_draw

    def _generate_gradient(self) -> Image.Image:
        """ "
        Generate the gradient background of the card.

        It generate a linear gradient with 2 colors depending on the type of the card.
        :return: The background image with the gradient.
        """
        if isinstance(self._card, AbstractCharacterCard):
            return self._generate_random_gradient_two_color(
                *self.resources.COLORS_BY_RACE[self._card.race]  # type: ignore
            )

        return self._generate_random_gradient_two_color(*self.resources.HUMAN_COLORS)

    def _generate_random_gradient_two_color(
        self,
        start_color: Tuple[int, int, int],
        end_color: Tuple[int, int, int],
    ) -> Image:
        """
        Generate a linear gradient with 2 colors.

        Create a linear gradient with the first color at the top left
        and the second color at the bottom right.

        :param start_color: The start color of the gradient.
        :param end_color: The end color of the gradient.
        :return: The gradient image.
        """
        gradient = Image.new("RGB", (self.resources.WIDTH, self.resources.HEIGHT))
        for x in range(self.resources.WIDTH):
            for y in range(self.resources.HEIGHT):
                color_nuance = (
                    start_color[0]
                    + int(
                        (end_color[0] - start_color[0])
                        * ((y + x) / (self.resources.HEIGHT + self.resources.WIDTH)),
                    ),
                    start_color[1]
                    + int(
                        (end_color[1] - start_color[1])
                        * ((y + x) / (self.resources.HEIGHT + self.resources.WIDTH)),
                    ),
                    start_color[2]
                    + int(
                        (end_color[2] - start_color[2])
                        * ((y + x) / (self.resources.HEIGHT + self.resources.WIDTH)),
                    ),
                )
                gradient.putpixel((x, y), color_nuance)
        gradient = gradient.filter(ImageFilter.GaussianBlur(radius=100))
        return gradient

    def _place_main_image(self) -> None:
        """
        Place the main image of the card on the image.

        It add rounded corners to the main image, add a small shadow behind it
        and paste it to the actual image.
        """
        # Round the corners of the main image
        self._card_img = self._card_img.convert("RGBA")
        self._card_img = self._card_img.resize(
            (
                self.resources.MAIN_IMAGE_WIDTH,
                self.resources.MAIN_IMAGE_HEIGHT,
            ),
        )

        # Add a shadow behind the main image
        shadow = Image.new(
            "RGBA",
            (
                self.resources.MAIN_IMAGE_WIDTH + 20,
                self.resources.MAIN_IMAGE_HEIGHT + 20,
            ),
            (0, 0, 0, 0),
        )
        shadow_draw = ImageDraw.Draw(shadow)
        shadow_draw.rounded_rectangle(
            (
                0,
                0,
                self.resources.MAIN_IMAGE_WIDTH + 20,
                self.resources.MAIN_IMAGE_HEIGHT + 20,
            ),
            self.resources.MAIN_IMAGE_RADIUS_CORNER,
            fill=(0, 0, 0, 100),
        )
        self._image.paste(
            shadow,
            (
                self.resources.MAIN_IMAGE_POSITION_X - 10,
                self.resources.MAIN_IMAGE_POSITION_Y - 10,
            ),
            shadow,
        )
        # Add a border to the main image
        border = Image.new(
            "RGBA",
            (
                self.resources.MAIN_IMAGE_WIDTH + 2,
                self.resources.MAIN_IMAGE_HEIGHT + 2,
            ),
            (255, 255, 255, 0),
        )
        border_draw = ImageDraw.Draw(border)
        border_draw.rounded_rectangle(
            (
                0,
                0,
                self.resources.MAIN_IMAGE_WIDTH + 2,
                self.resources.MAIN_IMAGE_HEIGHT + 2,
            ),
            self.resources.MAIN_IMAGE_RADIUS_CORNER,
            fill=(0, 0, 0, 255),
        )
        self._image.paste(
            border,
            (
                self.resources.MAIN_IMAGE_POSITION_X - 1,
                self.resources.MAIN_IMAGE_POSITION_Y - 1,
            ),
            border,
        )

        # Paste the main image to the actual image
        self._image.paste(
            self._card_img,
            (
                self.resources.MAIN_IMAGE_POSITION_X,
                self.resources.MAIN_IMAGE_POSITION_Y,
            ),
            self.resources.MAIN_IMAGE_MASK,
        )

    def _place_card_name(self) -> None:
        """
        Place the name of the card on the image.

        It add a shadow behind the name and paste it to the actual image.
        """
        image_name = self.resources.NAME_BACKGROUND.copy()
        draw = ImageDraw.Draw(image_name)
        # draw name at the center of this image
        name_text = self._card.name
        name_text_width, name_text_height = draw.textsize(
            name_text,
            font=self.resources.BIG_TEXT_FONT,
        )
        name_text_position_x = self.resources.NAME_WIDTH / 2 - name_text_width / 2
        name_text_position_y = self.resources.NAME_HEIGHT / 2 - name_text_height / 2
        # Paste the name to the actual image
        draw.text(
            (name_text_position_x, name_text_position_y),
            name_text,
            font=self.resources.BIG_TEXT_FONT,
            fill=self.resources.TEXT_COLOR,
            stroke_width=2,
            stroke_fill=self.resources.TEXT_STROKE_COLOR,
        )
        self._image.paste(
            image_name,
            (self.resources.NAME_POSITION_X, self.resources.NAME_POSITION_Y),
            image_name,
        )

    def _place_stats(self) -> None:
        """Place the stats of the card on the image."""
        self._image.paste(
            self.resources.STATS_BACKGROUND,
            self.resources.STATS_POSITION,
            self.resources.STATS_BACKGROUND,
        )

    def _place_card_description(self) -> None:
        """
        Place the description of the card on the image.

        It add a shadow behind the description and paste it to the actual image.
        """
        image = self.resources.DESCRIPTION_BACKGROUND.copy()
        draw = ImageDraw.Draw(image)
        # Draw the description
        font = self.resources.MEDIUM_TEXT_FONT
        text_list = get_text_list_fit_width(
            self._card.description,
            self.resources.DESCRIPTION_WIDTH - 2 * self.resources.DESCRIPTION_PADDING,
            font,
        )
        for i, text in enumerate(text_list):
            draw.text(
                (
                    self.resources.DESCRIPTION_PADDING,
                    self.resources.DESCRIPTION_PADDING
                    + i * self.resources.TEXT_NORMAL_SIZE,
                ),
                text,
                font=font,
                fill=self.resources.TEXT_COLOR,
                stroke_width=1,
                stroke_fill=self.resources.TEXT_STROKE_COLOR,
            )
        self._image.paste(
            image,
            self.resources.DESCRIPTION_POSITION,
            image,
        )

    def _place_card_rarity(self) -> None:
        """
        Place the rarity of the card on the image.

        Add a specific symbol and color on the card depending on the rarity.
        It must be aestic and not too much intrusive.
        It can be place in the bottom right corner of the card or top right.
        """
        rarity_symbol = self.resources.SYMBOL_BY_RARITY[self._card.rarity]
        self._image.paste(
            rarity_symbol,
            self.resources.RARITY_SYMBOL_POSITION,
            rarity_symbol,
        )
