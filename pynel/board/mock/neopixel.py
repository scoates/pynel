from img import serpentine
from context import Context


class MockNeoPixel:
    SCALE = 16  # scale the imgcat (iTerm2) display by this much

    def __init__(self, pin, num_pixels):
        self.pin = pin
        self.num_pixels = num_pixels
        self.pixels = [(0, 0, 0) for i in range(self.num_pixels)]
        self.config = Context.data["CONFIG"]

    def __getitem__(self, k):
        return self.pixels[k]

    def __setitem__(self, k, v):
        self.pixels[k] = v

    def __len__(self):
        return len(self.pixels)

    def write(self):
        print(f"writing… {len(self.pixels)} pixels")
        try:
            from imgcat import imgcat
        except ImportError:
            # imgcat not available; we're either on micropython or it's just not installed
            return
        from PIL import Image

        w = self.config["PIXELS_W"]
        h = self.config["PIXELS_H"]
        im = Image.new("RGB", (w, h))

        # de-serpentine if serpentined
        pixels = (
            serpentine(self.pixels, w, h) if self.config["SERPENTINE"] else self.pixels
        )
        im.putdata([tuple(p) for p in pixels])
        im = im.resize((w * self.SCALE, h * self.SCALE), Image.NEAREST)
        imgcat(im)
