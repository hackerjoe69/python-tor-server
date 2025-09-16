import asyncio
import aioredis
from app.config import settings

class RedisPubSub:
    def __init__(self):
        self.redis = None

    async def connect(self):
        self.redis = await aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", decode_responses=True)

    async def publish(self, room: str, message: str):
        await self.redis.publish(room, message)

    async def subscribe(self, room: str):
        pubsub = self.redis.pubsub()
        await pubsub.subscribe(room)
        return pubsub

redis_pubsub = RedisPubSub()
