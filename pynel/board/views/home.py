def view(pixels, scale, palette, view_img, w, h, r):
    ret = """<!DOCTYPE html>
<html lang="en">
  <head>
    <title>Pynel</title>
    <style>
      body {
        padding: 0;
        margin: 0;
      }
      #panel-img {
        user-select: none;
        height: 100vh;
      }
      #panel-img svg {
        height: 100vh;
        aspect-ratio: 1;
        width: auto;
      }
      #grid-container {
      /*
        display: grid;
        grid-template-columns: 3fr 1fr;
        grid-column-gap: {{scale}}px;
        max-width: 100%;
        height: 100vh;
    */
        display: flex;
        max-width: 100%;
        height: 100vh;
        width: 100vw;
        overflow: hidden;
        align-items: stretch;
        justify-content: stretch;
      }
      #palette {
        display: grid;
        align-items: start;
        height: 100vh;
        justify-content: stretch;
        grid-template-rows: {{scale}}fr 1fr;
        width: 100%;
      }
      #palette-colors {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        grid-auto-rows: 1fr;
        height: 100%;
      }
      #show {
        grid-gap 10px;
      }
      #show-button {
        height: 100%;
        width: 100%;
      }
      .pal-color {
        border: 1px solid black;
        padding: 0;
        box-model: inline-box;
        line-height: 0;
      }
      .pal-color.selected {
        padding: 0;
        border: {{scale}}px solid white;
      }""".replace(
        "{{scale}}", str(scale)
    )

    for n in range(0, len(palette), 2):
        pal = palette[n]
        ret += f"#pal_{n} {{ background-color: rgb({pal[0]}, {pal[1]}, {pal[2]});}}\n"
        pal = palette[n + 1]
        ret += f"#pal_{n+1} {{ background-color: rgb({pal[0]}, {pal[1]}, {pal[2]});}}\n"

    ret += """
    </style>
    <script>
      var palette = [];"""

    for pal in palette:
        ret += f"palette.push([{pal[0]}, {pal[1]}, {pal[2]}]);\n"

    ret += "var pixels = [];\n"

    for pix in pixels:
        ret += f"pixels.push([{pix[0]}, {pix[1]}, {pix[2]}]);\n"

    ret += """
      var current_color;

      var select_color = function(num) {
        window.current_color = palette[num];
        for (i=0; i<palette.length; i++) {
          var el = document.getElementById("pal_" + i);
          if (el) {
            if (i === num) {
              el.classList.add("selected");
            } else {
              el.classList.remove("selected");
            }
          }
        }
      };

      function redraw_pixels() {
        for (var i=0; i<pixels.length; i++) {
          var el = document.getElementById("pix_" + i);
          var pix = pixels[i];
          el.style.fill = "rgb(" + pix[0] + ", " + pix[1] + ", " + pix[2] + ")";
        }
      }

      var makePaletteClickHandler = function(num) {
        return function() {
          select_color(num);
        }
      };

      var makePixelClickHandler = function(num) {
        return function(e) {
          if (e.buttons === 1) {
              pixels[num] = current_color;
              redraw_pixels();
          } else if (e.buttons === 2) {
            pixels[num] = [0, 0, 0];
            redraw_pixels();
          }
        }
      };

      document.addEventListener("DOMContentLoaded", function() {
          select_color(0);
          for (var i=0; i<palette.length; i++) {
            var el = document.getElementById("pal_" + i);
            el.addEventListener("click", makePaletteClickHandler(i));
          }
          for (var i=0; i<pixels.length; i++) {
            var el = document.getElementById("pix_" + i);
            el.addEventListener("mousedown", makePixelClickHandler(i));
            el.addEventListener("mouseenter", makePixelClickHandler(i));
            el.addEventListener("contextmenu", e => {
              e.preventDefault();
            });
          }
          var el = document.getElementById("show");
          el.addEventListener("click", function(e) {
            fetch('/change', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify(pixels),
            })
            .then(response => response)
            .then(data => {
              console.log('Success:', data);
            })
            .catch((error) => {
              console.error('Error:', error);
            });

          });

        }
      );
    </script>
  </head>
  <body>
    <div id="grid-container">
      <div id="panel-img">"""
    ret += view_img(w=w, h=h, r=r, scale=scale, pixels=pixels)
    ret += """
      </div>
      <div id="palette">
        <div id="palette-colors">
          """
    for pal in range(len(palette)):
        ret += f'<div class="pal-color" id="pal_{pal}">&nbsp;</div>\n'

    ret += """
        </div>
        <div id="show"><button id="show-button">Show!</button></div>
      </div>
    </div>
  </body>
</html>
"""
    return ret
