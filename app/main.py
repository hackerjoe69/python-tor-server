from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import http_routes, ws_routes
from app.redis_pubsub import redis_pubsub

app = FastAPI(title="Realtime Anonymous Server")

# Routers
app.include_router(http_routes.router)
app.include_router(ws_routes.router)

# Static frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
async def startup_event():
    await redis_pubsub.connect()
