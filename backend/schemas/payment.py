"""Administracion de pagos.
"""
from sqlmodel import SQLModel, Field, Column, JSON
from typing import Optional, List
from datetime import datetime, timezone
from pydantic import BaseModel

class PaymentBase(SQLModel):
    user_id: Optional[int] = Field(index=True)
    amount: float  
    status: str    # "pending", "completed", "failed"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    gateway_transaction_id: Optional[str] = None 

class Payment(PaymentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    products_ids: List[int] = Field(default=[], sa_column=Column(JSON))

# Request
class PaymentRequest(BaseModel):
    """Entidad que envía el frontend para procesar el pago."""
    products_ids: List[int] 
    amount: float
    payment_token: str  

class PaymentUpsert(BaseModel): 
    """Entidad para actualizar un pago."""
    id: int 
    status: Optional[str] = None
    gateway_transaction_id: Optional[str] = None

class PaymentFilters(BaseModel):
    status: Optional[str] = None
    amount: Optional[float] = None
    date: Optional[datetime] = None 
    gateway_transaction_id: Optional[str] = None

# Response
class PaymentPublic(PaymentBase):
    """Entidad que se devuelve al frontend para no exponer datos internos."""
    id: int
    products_ids: List[int]
