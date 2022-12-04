import os
from functions import check_env
from static_router import static_router
from promo_router import promo_router
from fastapi import FastAPI
import uvicorn


check_env(
    "REDIS_CONNSTRING",
    "ADMIN_SECRET"
)


app = FastAPI(
    openapi_url=None,
    docs_url=None,
    redoc_url=None
)
app.include_router(static_router)
app.include_router(promo_router)


uvicorn.run(app, host="0.0.0.0", port=os.getenv("PORT", 8000))
