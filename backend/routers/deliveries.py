"""Cuando el cliente compra un producto y escoge esta opcion.
"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get():
    pass

@router.post("/")
async def create():
    pass
@router.patch("/")
async def partial_update():
    pass

@router.put("/")
async def update():
    pass

@router.delete("/")
async def delete():
    pass

