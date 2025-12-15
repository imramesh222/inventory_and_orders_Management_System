from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.routes import include_routers
from core.settings import Settings

app = FastAPI(title="Inventory & Orders Management API", version="1.0.0")

settings = Settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Root"])
async def hc():
    return {"error": False, "msg": "Ok", "result": {"status": "SERVING"}}

include_routers(app)