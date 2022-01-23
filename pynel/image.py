import sys
from PIL import Image
from board.util import get_config, write_image


CONFIG = get_config()

im = Image.open(sys.argv[1])

w = im.width
h = im.height

if w == CONFIG["PIXELS_W"] and h == CONFIG["PIXELS_H"]:
    # we got the right dimensions, so use the image:
    pixels = [list(i) for i in list(im.getdata())]
else:
    # empty image (all dark blue):
    pixels = [[0, 0, 32] for i in range(CONFIG["PIXELS_W"] * CONFIG["PIXELS_H"])]

write_image(pixels)
