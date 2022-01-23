from machine import Pin
from neopixel import NeoPixel

from util import get_config
from net import wifi_connect
from img import read_image, show_image
from web import Context


CONFIG = get_config()
num_pixels = CONFIG["PIXELS_W"] * CONFIG["PIXELS_H"]
NP = NeoPixel(Pin(CONFIG["DATA_PIN"]), num_pixels)

Context.data = dict(CONFIG=CONFIG, NP=NP)
show_image(read_image())

# after the panel is first initialized (because this wifi connection is slow)
wifi_connect(CONFIG)
