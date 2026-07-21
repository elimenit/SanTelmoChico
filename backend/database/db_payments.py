"""Interaccion con el servidor y pagos.
"""
from fastapi import HTTPException
from sqlmodel import SQLModel, Session
from redis import Redis
from schemas.payment import (
    Payment, PaymentUpsert, PaymentFilters,
    PaymentRequest, PaymentPublic
)
class DBPayments(SQLModel):

    def get_all(self, redis_client: Redis, session: Session, filters: PaymentFilters)-> list[PaymentPublic]:
        pass

    def get(self, redis_client: Redis, session: Session, payment: PaymentUpsert) -> PaymentPublic:
        pass

    def add(self, redis_client: Redis, session: Session, new_payment: PaymentRequest)-> None:

        pass
