import redis

from api.core import config

rd = redis.Redis(
    host=config.redis_host,
    port=config.redis_port,
    db=0
)