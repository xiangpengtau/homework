import redis
from .config import settings


redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)