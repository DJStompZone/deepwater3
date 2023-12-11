import colorsys
import math
from itertools import product

from PIL import Image, ImageDraw
from PIL.Image import Image as PILImageType


def build_colorwheel() -> PILImageType:
    """Builds a color wheel image."""

    def cartesian_to_polar(x: int, y: int) -> tuple[float, float]:
        r: float = math.sqrt(x**2 + y**2)
        theta: float = math.atan2(y, x)
        return r, theta

    def polar_to_hsl(
        r: float, theta: float, max_radius: float
    ) -> tuple[float, float, float]:
        hue: float = (theta + math.pi) / (2 * math.pi) * 360
        saturation: float = r / max_radius
        lightness = 0.5
        return hue, saturation, lightness

    def hsl_to_rgb(h: float, s: float, l: float) -> tuple[int, int, int]:
        r, g, b = colorsys.hls_to_rgb(h=h / 360, l=l, s=s)
        return int(r * 255), int(g * 255), int(b * 255)

    image_size = 256 * 3
    image: PILImageType = Image.new(
        mode="RGBA", size=(image_size, image_size), color=(0, 0, 0, 0)
    )
    draw: ImageDraw.ImageDraw = ImageDraw.Draw(image)
    center_x, center_y = image_size // 2, image_size // 2
    max_radius = image_size // 2

    for x, y in product(range(image_size), repeat=2):
        r, theta = cartesian_to_polar(x - center_x, y - center_y)
        if r <= max_radius:
            hue, saturation, lightness = polar_to_hsl(r, theta, max_radius)
            rgb_color: tuple[int, int, int] = hsl_to_rgb(hue, saturation, lightness)
            draw.point(xy=(x, y), fill=rgb_color)

    return image


if __name__ == "__main__":
    image = build_colorwheel()
    image.save("colorwheel.png")
