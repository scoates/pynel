from microdot import Microdot, Response
from context import Context
from img import read_image, write_image, show_image
from palette import PALETTE
from views.home import view as view_home
from views.img import view as view_img

app = Microdot()


@app.get("/")
def home(request):
    return Response(
        view_home(
            pixels=read_image(),
            scale=10,
            palette=PALETTE,
            view_img=view_img,
            w=Context.data["CONFIG"]["PIXELS_W"],
            h=Context.data["CONFIG"]["PIXELS_H"],
            r=2,
        ),
        200,
        {"Content-Type": "text/html"},
    )


@app.post("/change")
def change(request):
    if not request.json:
        return Response("Send JSON", 400)
    write_image(request.json, False)
    show_image(read_image())
    return "OK"


def serve(port=80):
    app.run(port=port, debug=True)
