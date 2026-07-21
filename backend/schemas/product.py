"""Produtos
"""
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from pydantic import ConfigDict, BaseModel

class ProductBase(SQLModel):
    code: str = Field(unique=True, index=True, max_length=50)
    name: str = Field(max_length=200)
    category: str = Field(max_length=100)
    marca: str = Field(max_length=100)
    material: str = Field(max_length=100)
    price: int = Field(gt=0)
    stock: int = Field(ge=0)
    image: Optional[str] = Field(default=None, max_length=100)
    description: Optional[str] = Field(default=None, max_length=1000)

# BD
class Product(ProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Request
class ProductCreate(ProductBase):
    image: str
    model_config = ConfigDict(extra='forbid')  # Zero Trust: rechazar campos extras

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=200)
    category: Optional[str] = Field(None, max_length=100)
    marca: Optional[str] = Field(None, max_length=100)
    material: Optional[str] = Field(None, max_length=100)
    price: Optional[int] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)

    description: Optional[str] = Field(None, max_length=1000)
    model_config = ConfigDict(extra='forbid')

class ProductUpsert(BaseModel):
    """Usado para validar IDs en rutas"""
    id: int = Field(gt=0)

class ProductFilters(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    category: Optional[str] = None
    marca: Optional[str] = None
    material: Optional[str] = None
    limit: int = Field(50, gt=0, le=200)  
    offset: int = Field(0, ge=0)
    
    model_config = ConfigDict(extra='forbid')

# Response
class ProductPublic(ProductBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
