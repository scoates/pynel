def view(w, h, r, scale, pixels):
    ret = ""
    ret += f'<svg id="panelimg" viewBox="0 0 {w * scale} {h * scale}" xmlns="http://www.w3.org/2000/svg" style="background-color: black;">\n'
    ret += """
    <style>
      rect {
        stroke: #111;
        stroke-width: {{r}};
      }
    </style>""".replace(
        "{{r}}", str(r)
    )
    for y in range(h):
        for x in range(w):
            pix = y * w + x
            ret += (
                f'<rect class="pixel" id="pix_{pix}" y="{y * scale}" x="{x * scale}" '
            )
            ret += f'width="{scale}" height="{scale}" rx="{r}"'
            ret += f'style="fill: rgb({pixels[pix][0]}, {pixels[pix][1]}, {pixels[pix][2]});"/>'
    ret += "</svg>"
    return ret
