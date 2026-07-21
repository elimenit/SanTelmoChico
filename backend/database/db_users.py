"""BD que administra o gestiona usuarios.
"""
import json
from fastapi import HTTPException, status
from sqlmodel import Session, select
from schemas.user import (
    User, UserCreate, UserPublic,
    UserFilters, UserUpdate
)
from redis import Redis 
class DBUsers:
    def __invalidate_caches(self, redis_client: Redis, user_id: int | None = None):
        """Invalida las listas y, opcionalmente, la caché de un usuario específico."""
        for key in redis_client.scan_iter("users:list:*"):
            redis_client.delete(key)
        
        if user_id:
            redis_client.delete(f"users:item:{user_id}")

    def __build_list_query(self, filters: UserFilters | None):
        query = select(User).where(User.is_active == True)
        if not filters:
            return query

        filter_dict = filters.model_dump(exclude={"limit", "offset"}, exclude_none=True)
        for key, val in filter_dict.items():
            if isinstance(val, str):
                safe_val = self.__escape_sql_wildcards(val)
                query = query.where(getattr(User, key).ilike(f"%{safe_val}%"))
            else:
                query = query.where(getattr(User, key) == val)
        return query

    def __escape_sql_wildcards(self, text: str) -> str:
        return text.replace("%", "\\%").replace("_", "\\_")

    def get_all(self, redis_client: Redis, filters: UserFilters, session: Session) -> list[UserPublic]:
        filter_str = filters.model_dump_json(exclude_none=True)
        cache_key = f"users:list:{filter_str}"

        cached_data = redis_client.get(cache_key)
        if cached_data:
            data_list = json.loads(cached_data)
            return [UserPublic.model_validate(item) for item in data_list]

        query = self.__build_list_query(filters)
        query = query.offset(filters.offset).limit(filters.limit)
        users = session.exec(query).all()
        
        users_dict_list = [u.model_dump(mode='json') for u in users]
        redis_client.set(cache_key, json.dumps(users_dict_list), ex=3600)

        return users

    def get(self, redis_client: Redis, user_id: int, session: Session) -> UserPublic:
        """Si existe el usuario en la cache lo devuelve sino lo cachea.
        """
        cache_key = f"users:item:{user_id}"
        
        cached_data = redis_client.get(cache_key)
        if cached_data:
            return UserPublic.model_validate(json.loads(cached_data))

        user = self.__get_by_id(session, user_id)
        
        redis_client.set(cache_key, json.dumps(user.model_dump(mode='json')), ex=3600)
        
        return UserPublic.model_validate(user)

    def add(self, redis_client: Redis, user: UserCreate, session: Session) -> UserPublic:
        existing = session.exec(select(User).where(User.email == user.email)).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El email ya está registrado."
            )

        new_user = User.model_validate(user)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        self.__invalidate_caches(redis_client)

        return UserPublic.model_validate(new_user)

    def update(self, redis_client: Redis, user_id: int, update_data: UserUpdate, session: Session) -> UserPublic:
        user = self.__get_by_id(session, user_id)
        update_dict = update_data.model_dump(exclude_unset=True)

        for key, value in update_dict.items():
            setattr(user, key, value)
        
        session.add(user)
        session.commit()
        session.refresh(user)

        self.__invalidate_caches(redis_client, user_id)

        return UserPublic.model_validate(user)

    def remove(self, redis_client: Redis, user_id: int, session: Session) -> UserPublic:
        """Soft Delete (recomendado Zero Trust)"""
        user = self.__get_by_id(session, user_id)
        user.is_active = False
        
        session.add(user)
        session.commit()
        session.refresh(user)

        self.__invalidate_caches(redis_client, user_id)

        return UserPublic.model_validate(user)

    # Privado!.
    def __get_by_id(self, session: Session, user_id: int) -> User:
        user = session.get(User, user_id)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        return user