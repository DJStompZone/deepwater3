import logging
from itertools import cycle

from PIL import Image

from stego_utils import RGBAPixelArray

logging.basicConfig(level=logging.DEBUG, filename="stego.log", filemode="w")
logger = logging.getLogger(__name__)


def encode_message(pix_array):
    test_str = (
        "This is a test. The quick brown fox jumped over the lazy dog. TESTING (!)"
    )
    idx = cycle(range(4))
    msg_cycle = cycle("".join([f"{ord(c):#010b}"[2:] for c in test_str]))
    remainder = 0
    modulus = 37
    for ci, column in enumerate(pix_array):
        logger.debug(f"Column {ci}: offset {remainder}")
        start_index = (modulus - remainder) % modulus
        logger.debug(f"Column {ci}: start index {start_index}")
        stego_bits = (len(column) - start_index + remainder) // modulus
        remainder = (len(column) + remainder) % modulus
        for i in range(stego_bits):
            target_pixel = start_index + (i * modulus)
            if target_pixel >= len(column):
                break
            target_channel = next(idx)
            set_bit = int(next(msg_cycle))
            # Clear the LSB of the pixel's color channel
            column[target_pixel][target_channel] &= 254
            # Set the LSB to the message bit
            column[target_pixel][target_channel] |= set_bit
            logger.debug(f" [c{ci}] Pixel {target_pixel}: {set_bit}")
        logger.debug(f"Finished column {ci} with offset {remainder}")


def decode_message(pix_array, modulus=37):
    decoded_bits = ""
    remainder = 0
    idx = cycle(range(4))

    for column in pix_array:
        # Calculate start index for this column
        start_index = (modulus - remainder) % modulus

        # Calculate stego bits, considering the start index
        stego_bits = (len(column) - start_index + remainder) // modulus

        for i in range(stego_bits):
            target_pixel = start_index + (i * modulus)
            if target_pixel >= len(column):
                break
            target_channel = next(idx)
            bit = column[target_pixel][target_channel] & 1
            decoded_bits += str(bit)

        # Update remainder for the next column
        remainder = (len(column) + remainder) % modulus

    # Convert binary string to text, ensuring complete 8-bit sequences
    decoded_text = ""
    for i in range(0, len(decoded_bits) - len(decoded_bits) % 8, 8):
        byte = decoded_bits[i : i + 8]
        decoded_text += chr(int(byte, 2))

    return decoded_text


if __name__ == "__main__":
    logger.info("Running stego_core.py")
    logger.info("Loading colorwheel.png")
    img = Image.open("colorwheel.png")
    logger.info("Converting to RGBAPixelArray")
    test = RGBAPixelArray.from_pillow(img)
    logger.info("Encoding message")
    encode_message(test)
    encoded = test.to_pillow()
    encoded.save("encoded.png")
    logger.info("Decoding message")
    decoded_message = decode_message(test)
    print("Decoded message: %s", decoded_message)
