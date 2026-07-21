"""Interaccion on el servidor de base de datos.
"""
from fastapi import HTTPException, status
from sqlmodel import SQLModel

class DBDeliveries(SQLModel):
    pass