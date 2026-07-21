"""Endpoints acerca del proceso de pago del cliente.
"""
from fastapi import APIRouter, Depends, status
from schemas.payment import (
    PaymentFilters, PaymentPublic, PaymentRequest, PaymentUpsert
)
from dependencies.database import DBPaymentsDep
from dependencies.dbsession import SessionDep
from dependencies.redis_session import RedisClientDep

router = APIRouter()

@router.get("/", response_model=list[PaymentPublic], status_code=status.HTTP_200_OK)
async def get_all():
    pass

@router.post("/buy")
async def buy_product(request: PaymentRequest):
    order_id = 12345 
    
    # 2. Preparar los datos para el email
    email_data = {
        "user_email": "usuario@ejemplo.com", # Esto vendría de tu DB o del token auth
        "order_id": order_id,
        "product_name": "Laptop XYZ",
        "total_price": 1500.00
    }
    
    # 3. Enviar evento a Kafka al topic "order_receipts"
    # await send_email_event(topic="order_receipts", data=email_data)
    
    return {"message": "Compra realizada con éxito. Recibirás un recibo por email."}

