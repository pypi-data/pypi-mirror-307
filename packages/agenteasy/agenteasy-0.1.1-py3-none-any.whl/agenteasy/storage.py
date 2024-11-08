from pydantic import BaseModel
from .agent import AIAgent
import redis


class StorageRedis(BaseModel):
    url: str


def setup_storage(agent: AIAgent, storage_backend: StorageRedis):
    _redis = redis.from_url(storage_backend.url)
    agent._store_backend = _redis
