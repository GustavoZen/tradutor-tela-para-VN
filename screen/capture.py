import mss
from PIL import Image


def capture_region(x, y, width, height):
    with mss.mss() as sct:
        monitor = {
            "left": x,
            "top": y,
            "width": width,
            "height": height,
        }

        screenshot = sct.grab(monitor)

        return Image.frombytes(
            "RGB",
            screenshot.size,
            screenshot.rgb
        )
