"""Obtiene una Dependencia global para poder hacer uso de redis para cachear en RAM.
"""
import os
import redis
from typing import Annotated, Generator
from fastapi import Depends
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("SERVER_REDIS")
REDIS_PORT = os.getenv("PORT_REDIS")

if not REDIS_HOST or not REDIS_PORT:
    raise ValueError("Variables de entorno REDIS_PORT o REDIS_HOST no configurados!!")

redis_pool = redis.ConnectionPool(
    host=REDIS_HOST, 
    port=REDIS_PORT, 
    db=0, 
    decode_responses=True
)

redis_client = redis.Redis(connection_pool=redis_pool)

def get_redis() -> Generator[redis.Redis, None, None]:
    try:
        yield redis_client
    finally:
        pass

RedisClientDep = Annotated[redis.Redis, Depends(get_redis)]