import colorsys
import math
from itertools import product

import numpy as np
from PIL import Image, ImageDraw
from PIL.Image import Image as PILImageType


class RGBAPixelArray(np.ndarray):
    def __new__(cls, input_array):
        # Input_array is an array-like object
        # Ensure input_array is a numpy array
        obj = np.asarray(input_array).view(cls)
        return obj

    def __array_finalize__(self, obj):
        # Called every time the object is created or viewed
        if obj is None:
            return

    @classmethod
    def from_pillow(cls, image):
        # Convert a PIL Image to RGBAPixelArray
        array = np.array(image)
        return cls(array)

    def to_pillow(self):
        # Convert RGBAPixelArray to a PIL Image
        return Image.fromarray(self, "RGBA")
