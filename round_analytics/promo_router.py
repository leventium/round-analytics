import os
from urllib.parse import parse_qs
import responses
from redis_interface import RedisStorage
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from jinja2 import Template


promo_router = APIRouter()
cur_dir = os.path.dirname(__file__)
with open(f"{cur_dir}/templates/promo_admin.html", "r") as file:
    admin_tmpl = Template(file.read())
with open(f"{cur_dir}/templates/promo.html", "r") as file:
    promo_tmpl = Template(file.read())


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
        return responses.ADMIN_NOT_FOUND
    inviters = await redis.get_inviters()
    inviter_stats = await redis.get_visit_stats()
    clients = await redis.get_contacts()
    panel = admin_tmpl.render(
        secret=secret,
        inviters=inviters,
        inviter_stats=inviter_stats,
        clients=clients
    )
    return HTMLResponse(content=panel)


@promo_router.post("/promo-admin/{secret}")
async def post_new_inviter(secret: str, req: Request):
    if secret != os.environ["ADMIN_SECRET"]:
        return responses.ADMIN_NOT_FOUND
    inviter = parse_qs((await req.body()).decode()).get("name")
    if inviter is not None:
        await redis.put_inviter(inviter[0])
    inviters = await redis.get_inviters()
    inviter_stats = await redis.get_visit_stats()
    clients = await redis.get_contacts()
    panel = admin_tmpl.render(
        secret=secret,
        inviters=inviters,
        inviter_stats=inviter_stats,
        clients=clients
    )
    return HTMLResponse(content=panel)


@promo_router.get("/promo")
async def get_promo_page(source: str):
    if source == "":
        return responses.NOT_FOUND
    if not await redis.check_inviter(source):
        return responses.BAD_REQUEST
    await redis.increase_visits(source)
    promo_site = promo_tmpl.render(
        callback_link=f"/promo?source={source}"
    )
    return HTMLResponse(content=promo_site)


@promo_router.post("/promo")
async def post_contacts(source: str, req: Request):
    if source == "":
        return responses.NOT_FOUND
    if not await redis.check_inviter(source):
        return responses.BAD_REQUEST
    body = parse_qs((await req.body()).decode())
    if "name" not in body or "contact" not in body:
        return responses.BAD_REQUEST
    await redis.increase_downloads(source)
    await redis.put_contact(source, body["name"][0], body["contact"][0])
    return HTMLResponse(content=responses.DOWNLOAD)
