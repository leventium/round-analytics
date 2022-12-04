import os
from fastapi import status
from fastapi.responses import JSONResponse, HTMLResponse, Response

cur_dir = os.path.dirname(__file__)

with open(f"{cur_dir}/static/error_404.html", "r") as file:
    ERR404 = file.read()

with open(f"{cur_dir}/static/piter.pdf", "rb") as file:
    guide = file.read()

with open(f"{cur_dir}/static/bootstrap.min.css", "r") as file:
    bootstrap = file.read()

with open(f"{cur_dir}/static/cover.css", "r") as file:
    cover = file.read()

with open(f"{cur_dir}/static/error_400.html", "r") as file:
    ERR400 = file.read()

with open(f"{cur_dir}/static/about.html", "r") as file:
    ABOUT = file.read()

with open(f"{cur_dir}/static/index.html", "r") as file:
    INDEX = file.read()

with open(f"{cur_dir}/static/void_page.html", "r") as file:
    VOID = file.read()

with open(f"{cur_dir}/static/download.html", "r") as file:
    DOWNLOAD = file.read()

css = {
    "bootstrap.min.css": bootstrap,
    "cover.css": cover
}

ADMIN_NOT_FOUND = JSONResponse(
    status_code=status.HTTP_404_NOT_FOUND,
    content={"detail": "not found"},
    media_type="application/json"
)

NOT_FOUND = HTMLResponse(
    status_code=status.HTTP_404_NOT_FOUND,
    content=ERR404
)

BAD_REQUEST = HTMLResponse(
    status_code=status.HTTP_400_BAD_REQUEST,
    content=ERR400
)

GUIDE = Response(
    content=guide,
    media_type="application/pdf"
)


def get_css(name: str):
    file = css.get(name)
    if file is None:
        return NOT_FOUND
    return Response(
        content=file,
        media_type="text/css"
    )
