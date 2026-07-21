from arq.connections import RedisSettings
from utils.constants import SERVER_REDIS, PORT_REDIS

redis_settings = RedisSettings(
    host=SERVER_REDIS or 'localhost',
    port=int(PORT_REDIS) if PORT_REDIS else 6379,
)