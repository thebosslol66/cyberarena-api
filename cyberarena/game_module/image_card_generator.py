# pragma: no cover
# flake8: noqa
import logging
from typing import List, Tuple

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from cyberarena.game_module.card.card_info import InfoCard
from cyberarena.game_module.card.enums import ObjectCardRace, ObjectCardType

logger = logging.getLogger("cyberarena.game_module.image_generator")


def get_text_list_fit_width(
    text: str,
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
    text_list.append("")
    for word in text.split(" "):
        if font.getsize(text_list[-1] + " " + word)[0] <= width:
            text_list[-1] += " " + word
        else:
            text_list.append(word)
    return text_list


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
    TEXT_BIG_SIZE = 50
    TEXT_NORMAL_SIZE = 30

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

    BIG_TEXT_FONT = ImageFont.truetype("arial.ttf", TEXT_BIG_SIZE)
    MEDIUM_TEXT_FONT = ImageFont.truetype("arial.ttf", TEXT_NORMAL_SIZE)

    DESCRIPTION_POSITION = (
        int((WIDTH - MAIN_IMAGE_WIDTH) / 2),
        MAIN_IMAGE_POSITION_Y + MAIN_IMAGE_HEIGHT + 50 + STATS_HEIGHT + 50,
    )

    DESCRIPTION_WIDTH = MAIN_IMAGE_WIDTH
    DESCRIPTION_HEIGHT = 200
    DESCRIPTION_BACKGROUND = Image.new(
        "RGBA",
        (DESCRIPTION_WIDTH, DESCRIPTION_HEIGHT),
        (255, 255, 255, 0),
    )
    DESCRIPTION_PADDING = 25

    RARITY_POSITION = (
        int((WIDTH - MAIN_IMAGE_WIDTH) / 2),
        MAIN_IMAGE_POSITION_Y
        + MAIN_IMAGE_HEIGHT
        + 50
        + STATS_HEIGHT
        + 50
        + DESCRIPTION_HEIGHT
        + 50,
    )

    def __init__(self) -> None:
        """Init the ImageCardGeneratorResources class."""
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

    def __init__(self, card: InfoCard, image_path: str) -> None:
        """
        Constructor.

        :param card: The card with all data to build the image.
        :param image_path: The path to the image of the card.
        """

        self._card: InfoCard = card
        self._card_img: Image = Image.open(image_path)

        (self._image, self._image_draw) = self._generate_base_image()

    def generate_card(self) -> Image.Image:
        """
        Generate the card image for a given card.

        :return: The image of the card fully build.
        """
        self._place_main_image()
        self._place_card_name()
        self._place_stats()
        self._place_card_description()
        return self._image

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
        if self._card.type == ObjectCardType.CHARACTER:
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
