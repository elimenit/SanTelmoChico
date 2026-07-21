"""Agrupa Los ApiRouters para que sea esacalable
"""
from fastapi import APIRouter

from routers import auth, reviews, products, payments, deliveries
from routers.admin import users

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["autenticacion"])
api_router.include_router(users.router, prefix="/users", tags=["usuarios"])
api_router.include_router(reviews.router, prefix="/reviews", tags=["resenas"])
api_router.include_router(products.router, prefix="/products", tags=["productos"])
api_router.include_router(payments.router, prefix="/payments", tags=["pagos"])
api_router.include_router(deliveries.router, prefix="/deliveries", tags=["deliveris"])