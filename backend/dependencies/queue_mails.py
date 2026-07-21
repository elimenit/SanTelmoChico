"""Redis + ARQ -> Cola de mensajeria.
"""
from arq.connections import ArqRedis

redis_pool: ArqRedis | None = None

async def get_redis_pool() -> ArqRedis:
    """Dependencia para inyectar el pool de Redis en las rutas.
    """
    
    if redis_pool is None:
        raise RuntimeError("El pool de Redis no está inicializado")
    return redis_pool