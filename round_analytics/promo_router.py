import os
from urllib.parse import parse_qs
import static
import templates
from redis_interface import RedisStorage
from functions import check_env
from fastapi import APIRouter, Request, status, Response
from fastapi.responses import HTMLResponse
from jinja2 import Template


check_env(
    "REDIS_CONNSTRING",
    "ADMIN_SECRET"
)
promo_router = APIRouter()
promo_tmpl = Template(templates.PROMO)
admin_tmpl = Template(templates.ADMIN)


@promo_router.on_event("startup")
async def start():
    global redis
    redis = await RedisStorage.create(os.environ["REDIS_CONNSTRING"])


@promo_router.on_event("shutdown")
async def stop():
    global redis
    await redis.close()


@promo_router.get("/promo-admin/{secret}")
async def get_admin_panel(secret: str):
    if secret != os.environ["ADMIN_SECRET"]:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "not found"},
            media_type="application/json"
        )
    inviters = await redis.get_inviters()
    inviter_stats = await redis.get_visit_stats()
    clients = await redis.get_contacts()
    panel = await admin_tmpl.render_async(
        secret=secret,
        inviters=inviters,
        inviter_stats=inviter_stats,
        clients=clients
    )
    return HTMLResponse(content=panel)


@promo_router.post("/promo-admin/{secret}")
async def post_new_inviter(secret: str, req: Request):
    if secret != os.environ["ADMIN_SECRET"]:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "not found"},
            media_type="application/json"
        )
    body = parse_qs((await req.body()).decode())
    await redis.put_inviter(body["name"][0])
    inviters = await redis.get_inviters()
    inviter_stats = await redis.get_visit_stats()
    clients = await redis.get_contacts()
    panel = await admin_tmpl.render_async(
        secret=secret,
        inviters=inviters,
        inviter_stats=inviter_stats,
        clients=clients
    )
    return HTMLResponse(content=panel)


@promo_router.get("/promo")
async def get_promo_page(source: str | None = None):
    if source is None:
        return HTMLResponse(
            content=static.ERR404,
            status_code=status.HTTP_404_NOT_FOUND
        )
    if redis.check_inviter(source):
        return HTMLResponse(
            content=static.ERR400,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    await redis.increase_visits(source)
    return await promo_tmpl.render_async(
        callback_link=f"https://round-travel.site/promo?source={source}"
    )


@promo_router.post("/promo")
async def post_contacts(source: str, req: Request):
    if redis.check_inviter(source):
        return HTMLResponse(
            content=static.ERR400,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    body = parse_qs((await req.body()).decode())
    if "name" not in body or "contact" not in body:
        return HTMLResponse(
            content=static.ERR400,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    await redis.increase_downloads(source)
    await redis.put_contact(source, body["name"][0], contact["contact"][0])
    return HTMLResponse(
        content=static.DOWNLOAD
    )
