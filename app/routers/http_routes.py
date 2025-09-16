from fastapi import APIRouter
from app.config import settings

router = APIRouter()

@router.get("/health")
async def healthcheck():
    return {"status": "ok"}

@router.get("/onion-info")
async def onion_info():
    try:
        with open(settings.TOR_HOSTNAME_PATH, "r") as f:
            onion = f.read().strip()
        return {"onion_address": onion}
    except FileNotFoundError:
        return {"error": "Tor hostname not found"}
