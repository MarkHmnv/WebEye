import redis

from api.core import config

rd = redis.Redis(
    password=config.redis_password,
    host=config.redis_host,
    port=config.redis_port,
)