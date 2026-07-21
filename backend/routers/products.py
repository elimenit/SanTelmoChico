"""Endpoints de los productos.
"""
from fastapi import APIRouter, Depends, Query, Body, status, Security
from schemas.product import ProductCreate, ProductFilters, ProductPublic, ProductUpdate, ProductUpsert
from dependencies.dbsession import SessionDep
from dependencies.database import DBProductsDep
from dependencies.auth import get_current_user, require_role
from dependencies.redis_session import RedisClientDep

router = APIRouter()

@router.get("/", response_model=list[ProductPublic])
async def get_all(
        redis_client: RedisClientDep,
        session: SessionDep,
        db: DBProductsDep,
        filters: ProductFilters = Query(),):
    return db.get_all(redis_client, filters, session)

@router.get("/{id}", response_model=ProductPublic)
async def get_one(
        id: int,
        redis_client: RedisClientDep,
        session: SessionDep,
        db: DBProductsDep,):

    return db.get(redis_client, ProductUpsert(id=id), session)

# === Solo personal autorizado ===
@router.post("/", response_model=ProductPublic, status_code=status.HTTP_201_CREATED)
async def create(
        redis_client: RedisClientDep,
        product: ProductCreate = Body(...),
        session: SessionDep = None,
        db: DBProductsDep = None,
        admin=Depends(require_role("admin"))):
        
    return db.add(redis_client, product, session)

@router.put("/{id}", response_model=ProductPublic)
async def update(
        id: int,
        redis_client: RedisClientDep,
        update_product: ProductUpdate = Body(...),
        session: SessionDep = None,
        db: DBProductsDep = None,
        admin=Depends(require_role("admin"))):

    return db.update(redis_client, ProductUpsert(id=id), update_product, session)

@router.delete("/{id}", response_model=ProductPublic)
async def delete(
    id: int,
    redis_client: RedisClientDep,
    session: SessionDep = None,
    db: DBProductsDep = None,
    admin=Depends(require_role("admin"))):

    return db.remove(redis_client, ProductUpsert(id=id), session)