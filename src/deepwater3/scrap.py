import colorsys
import math
from itertools import product

from PIL import Image, ImageDraw
from PIL.Image import Image as PILImageType

SQUARE_SIZE = 9
SQUARES_PER_ROW = 9


def create_square(r: int, g: int, b: int) -> PILImageType:
    img = Image.new("RGB", (SQUARE_SIZE, SQUARE_SIZE), (r, g, b))
    return img


def build_image_greenpink(squares_per_row: int) -> PILImageType:
    img = Image.new(
        "RGB", (SQUARE_SIZE * squares_per_row, SQUARE_SIZE * squares_per_row)
    )
    increment = 255 / (squares_per_row - 1)

    for i in range(squares_per_row**2):
        row, col = divmod(i, squares_per_row)
        r = int(increment * row)
        g = int(increment * col)
        b = int(increment * (row + col) // 2)
        square = create_square(r, g, b)
        img.paste(square, (col * SQUARE_SIZE, row * SQUARE_SIZE))

    return img


def build_image_redgreen(squares_per_row: int) -> PILImageType:
    img = Image.new(
        "RGB", (SQUARE_SIZE * squares_per_row, SQUARE_SIZE * squares_per_row)
    )
    red_increment = 255 / (squares_per_row - 1)
    green_increment = 255 / (squares_per_row - 1)
    blue_increment = 255 / (squares_per_row - 1)

    for i in range(squares_per_row):
        for j in range(squares_per_row):
            r = int(red_increment * i)
            g = int(green_increment * j)
            b = int(blue_increment * min(i, j))
            img.paste(
                (r, g, b),
                (
                    i * SQUARE_SIZE,
                    j * SQUARE_SIZE,
                    (i + 1) * SQUARE_SIZE,
                    (j + 1) * SQUARE_SIZE,
                ),
            )

    return img


full_image_greenpink = build_image_greenpink(SQUARES_PER_ROW)

full_image_redgreen = build_image_redgreen(SQUARES_PER_ROW)
