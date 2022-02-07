from microdot import Microdot, Response
from context import Context
from img import read_image, write_image, show_image
from palette import PALETTE
from util import get_dir

app = Microdot()


@app.get("/")
def home(request):
    with open(get_dir(__file__) + "/views/home.html") as f:
        return Response(
            f.read(),
            200,
            {"Content-Type": "text/html"},
        )


@app.get("/config")
def config(request):
    return Response(
        {
            "scale": 10,
            "w": Context.data["CONFIG"]["PIXELS_W"],
            "h": Context.data["CONFIG"]["PIXELS_H"],
        }
    )


@app.get("/pixels")
def pixels(request):
    return Response(read_image())


@app.get("/palette")
def palette(request):
    return Response(PALETTE)


@app.post("/change")
def change(request):
    if not request.json:
        return Response("Send JSON", 400)
    write_image(request.json, False)
    show_image(read_image())
    return "OK"


def serve(port=80):
    app.run(port=port, debug=True)
