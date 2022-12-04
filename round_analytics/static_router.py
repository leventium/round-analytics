import responses
from fastapi import APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse


static_router = APIRouter()


@static_router.get("/")
async def get_root_page():
    return RedirectResponse("/main")


@static_router.get("/main")
async def get_main_page():
    return HTMLResponse(content=responses.INDEX)


@static_router.get("/void")
async def get_void_page():
    return HTMLResponse(content=responses.VOID)


@static_router.get("/about")
async def get_about_page():
    return HTMLResponse(content=responses.ABOUT)


@static_router.get("/static/{name}")
async def get_static_file(name: str):
    return responses.get_css(name)


@static_router.get("/download")
async def get_file():
    return responses.GUIDE
