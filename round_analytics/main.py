import os
from static_router import static_router
from promo_router import promo_router
from fastapi import FastAPI
import uvicorn


app = FastAPI(
    openapi_url=None,
    docs_url=None,
    redoc_url=None
)
app.include_router(static_router)
app.include_router(promo_router)


uvicorn.run(app, host="0.0.0.0", port=os.getenv("PORT", 8000))
