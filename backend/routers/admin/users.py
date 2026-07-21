from fastapi import APIRouter, Path, Body, Query, status, Depends
from dependencies.dbsession import SessionDep
from dependencies.database import DBUsersDep
from dependencies.redis_session import RedisClientDep
from typing import Annotated

from schemas.user import (
    UserFilters, UserCreate, UserUpdate, UserPublic, User
)
from schemas.error import Error
from utils.auth import get_current_admin

router = APIRouter(dependencies=[Depends(get_current_admin)])

@router.get("/", response_model=list[UserPublic], responses={status.HTTP_404_NOT_FOUND: {"model": Error}})
async def all_users(redis_client: RedisClientDep, session: SessionDep, db: DBUsersDep, users_filters: Annotated[UserFilters, Query()]):
    return db.get_all(redis_client, session, users_filters)

@router.post("/", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def create_user(redis_client: RedisClientDep, session: SessionDep, db: DBUsersDep, user_create: Annotated[UserCreate, Body()]):
    return db.add(redis_client, session, user_create)

@router.patch("/{user_id}", response_model=UserPublic)
async def partial_update(
    user_id: Annotated[int, Path()], 
    user_update: Annotated[UserUpdate, Body()], 
    session: SessionDep, 
    db: DBUsersDep
):
    return db.update(redis_client, session, user_id, user_update)

@router.delete("/{user_id}", response_model=UserPublic)
async def delete_user(
    user_id: Annotated[int, Path()], 
    session: SessionDep, 
    db: DBUsersDep
):
    return db.remove(redis_client, session, user_id)