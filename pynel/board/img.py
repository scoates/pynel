from util import get_path
from context import Context


def write_image(pixels, verify=False):
    dat = b""
    for n, p in enumerate(pixels):
        for i in range(3):
            # micropython doesn't like this keyword argument
            try:
                dat += p[i].to_bytes(1, "big", False)
            except TypeError:
                dat += p[i].to_bytes(1, "big", signed=False)

    img_file = get_path(__file__, "image.dat")

    with open(img_file, "wb") as f:
        f.write(dat)

    print(f"Wrote {len(pixels)} pixels; buffer of ({len(dat)} bytes).")

    if verify:
        read_pixels = read_image()
        assert pixels == read_pixels, "Pixels match"
        print("Verified.")


def read_image(
    filename="image.dat", allow_default=True, default_filename="image_default.dat"
):
    img_file = get_path(__file__, filename)
    pixels = []
    try:
        with open(img_file, "rb") as f:
            r_p = f.read()
            num = len(r_p)
            print(f"read {num} bytes")
            for count in range(0, num, 3):
                p = [r_p[count], r_p[count + 1], r_p[count + 2]]
                pixels.append(p)
        return pixels
    except FileNotFoundError:
        if not allow_default:
            raise
        print(f"{filename} not found; trying {default_filename}")
        return read_image(filename=default_filename, allow_default=False)


def serpentine(pixels, w, h):
    for row in range(0, h, 2):
        row_start = row * w
        row_end = row_start + w
        pixels[row_start:row_end] = list(reversed(pixels[row_start:row_end]))
    return pixels


def _truncate_round(val):
    if val < 0:
        return 0
    if val > 255:
        return 255
    return round(val)


def show_image(pixels):
    w = Context.data["CONFIG"]["PIXELS_W"]
    h = Context.data["CONFIG"]["PIXELS_H"]
    np = Context.data["NP"]
    if Context.data["CONFIG"]["SERPENTINE"]:
        pixels = serpentine(pixels, w, h)
    for n in range(w * h):
        np[n] = [
            _truncate_round(pixels[n][0] * (Context.data["CONFIG"]["BRIGHTNESS"] / 100)),
            _truncate_round(pixels[n][1] * (Context.data["CONFIG"]["BRIGHTNESS"] / 100)),
            _truncate_round(pixels[n][2] * (Context.data["CONFIG"]["BRIGHTNESS"] / 100)),
        ]
        print(f"setting Pixel {n} to {np[n]}")

    np.write()
