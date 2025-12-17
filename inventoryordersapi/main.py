from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from inventoryordersapi.api.routes import include_routers
from inventoryordersapi.core.settings import settings

app = FastAPI(title="Inventory & Orders Management API", version="1.0.0")

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

from inventoryordersapi.api.routes.item_routes import router as item_router
app.include_router(item_router, prefix="/items", tags=["Items"])
