import sys
import os

DIR = "/".join(__file__.split("/")[:-1])
sys.path.append("/".join([DIR, "board"]))

from util import get_config
from img import read_image, show_image
from mock.neopixel import MockNeoPixel
from context import Context
from web import serve

CONFIG = get_config("/".join([DIR, "board", "config.json"]))

try:
    brightness = int(sys.argv[1])
    CONFIG["BRIGHTNESS"] = brightness
except (IndexError, ValueError):
    pass

Context.data["CONFIG"] = CONFIG
Context.data["NP"] = MockNeoPixel(
    CONFIG["DATA_PIN"], CONFIG["PIXELS_W"] * CONFIG["PIXELS_H"]
)

show_image(read_image())

serve(int(os.getenv("SIMULATE_PORT") or 8100))
