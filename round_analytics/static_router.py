import static
from fastapi import APIRouter, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse


static_router = APIRouter()
static_files = {
    "bootstrap.min.css": static.BOOTSTRAP,
    "cover.css": static.COVER
}
with open("piter.pdf", "rb") as file:
    guide = file.read()


@static_router.get("/")
async def get_root_page():
    return RedirectResponse(
        "https://round-travel.site/main",
        status_code=status.HTTP_302_FOUND
    )


@static_router.get("/main")
async def get_main_page():
    return HTMLResponse(content=static.INDEX)


@static_router.get("/void")
async def get_void_page():
    return HTMLResponse(content=static.VOID)


@static_router.get("/about")
async def get_about_page():
    return HTMLResponse(content=static.ABOUT)


@static_router.get("/static/{name}")
async def get_static_file(name: str):
    css = static_files.get(name)
    if css is None:
        return HTMLResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=static.ERR404
        )
    return Response(
        content=static_files,
        media_type="text/css"
    )


@static_router.get("/download")
async def get_file():
    return Response(
        content=guide,
        media_type="application/pdf"
    )
