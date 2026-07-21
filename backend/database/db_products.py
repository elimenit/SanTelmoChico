""" Interaccion con la BD acerca de los Productos.
"""
import json
from datetime import datetime
from fastapi import HTTPException, status
from sqlmodel import Session, select
from redis import Redis

from schemas.product import (
    Product, ProductCreate, ProductPublic,
    ProductFilters, ProductUpdate, ProductUpsert
)

class DBProducts:
    def __invalidate_caches(self, redis_client: Redis, product_id: int | None = None):
        """Invalida las listas y, opcionalmente, la caché de un producto específico."""
        for key in redis_client.scan_iter("products:list:*"):
            redis_client.delete(key)
            
        if product_id:
            redis_client.delete(f"products:item:{product_id}")

    def __build_list_query(self, filters: ProductFilters | None):
        """Construye la consulta de SQLAlchemy base sin ejecutarla."""
        query = select(Product).where(Product.is_active == True)
        if not filters:
            return query

        filter_dict = filters.model_dump(exclude={"limit", "offset"}, exclude_none=True)
        for key, val in filter_dict.items():
            if isinstance(val, str):
                safe_val = self.__escape_sql_wildcards(val)
                query = query.where(getattr(Product, key).ilike(f"%{safe_val}%"))
            else:
                query = query.where(getattr(Product, key) == val)
        return query

    def __escape_sql_wildcards(self, text: str) -> str:
        return text.replace("%", "\\%").replace("_", "\\_")

    # --- MÉTODOS HTTP GET (100% CACHEADOS EN REDIS) ---

    def get_all(self, redis_client: Redis, filters: ProductFilters, session: Session) -> list[ProductPublic]:
        """ Cachea en memoria, genera una clave unica -> intenta recupar desde redis
        -> guarda el resultado en redis -> devuelve desde redis.
        """
        filter_str = filters.model_dump_json(exclude_none=True)
        cache_key = f"products:list:{filter_str}"

        cached_data = redis_client.get(cache_key)
        if cached_data:
            # Deserializar el string JSON de vuelta a los esquemas de Pydantic
            data_list = json.loads(cached_data)
            return [ProductPublic.model_validate(item) for item in data_list]

        query = self.__build_list_query(filters)
        query = query.offset(filters.offset).limit(filters.limit)
        products = session.exec(query).all()
        
        products_dict_list = [p.model_dump(mode='json') for p in products]
        
        redis_client.set(cache_key, json.dumps(products_dict_list), ex=3600)

        return products
    
    def get(self, redis_client: Redis, id_obj: ProductUpsert, session: Session) -> ProductPublic:
        cache_key = f"products:item:{id_obj.id}"
        
        cached_data = redis_client.get(cache_key)
        if cached_data:
            return ProductPublic.model_validate(json.loads(cached_data))

        product = self.__get_by_id(session, id_obj.id)
        
        redis_client.set(cache_key, json.dumps(product.model_dump(mode='json')), ex=3600)
        
        return ProductPublic.model_validate(product)

    def add(self, redis_client: Redis, product: ProductCreate, session: Session) -> ProductPublic:
        """Invalida Cache.
        """
        existing = session.exec(
            select(Product).where(Product.code == product.code)
        ).first()
        if existing and existing.is_active:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El código de producto ya está registrado."
            )

        new_product = Product.model_validate(product)
        session.add(new_product)
        session.commit()
        session.refresh(new_product)

        self.__invalidate_caches(redis_client)

        return ProductPublic.model_validate(new_product)

    def update(self, redis_client: Redis, id_obj: ProductUpsert, update_product: ProductUpdate, session: Session) -> ProductPublic:
        """Invalida Cache.
        """
        product = self.__get_by_id(session, id_obj.id)
        update_data = update_product.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(product, key, value)
        
        product.updated_at = datetime.now()

        session.add(product)
        session.commit()
        session.refresh(product)

        self.__invalidate_caches(redis_client, product.id)

        return ProductPublic.model_validate(product)

    def remove(self, redis_client: Redis, id_obj: ProductUpsert, session: Session) -> ProductPublic:
        """Soft Delete (recomendado Zero Trust)"""
        product = self.__get_by_id(session, id_obj.id)
        product.is_active = False
        product.updated_at = datetime.now()

        session.add(product)
        session.commit()
        session.refresh(product)

        self.__invalidate_caches(redis_client, product.id)

        return ProductPublic.model_validate(product)
    
    # Privados
    def __get_by_id(self, session: Session, product_id: int) -> Product:
        product = session.get(Product, product_id)
        if not product or not product.is_active:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado"
            )
        return product