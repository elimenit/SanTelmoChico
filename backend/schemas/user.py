"""Administracion de usuarios.
"""
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr, ConfigDict

class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    username: str = Field(max_length=50, index=True)

# BD
class User(UserBase, table=True):
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    password: str = Field(max_length=255) 
    role: str = Field(default="user", max_length=20)
    reviews: List["Review"] = Relationship(back_populates="user")
    is_active: bool = Field(default=True)
    
# Request

class UserCreate(UserBase):
    """Payload para registrar usuarios."""
    password: str = Field(min_length=8, max_length=128)


class UserUpdate(SQLModel):
    """Payload para peticiones PATCH."""
    email: Optional[EmailStr] = Field(default=None, max_length=255)
    username: Optional[str] = Field(default=None, max_length=50)
    role: Optional[str] = Field(default=None, max_length=20)
    is_active: Optional[bool] = Field(default=None)

class UserFilters(SQLModel):
    """
    Validación estricta de Query Parameters.
    """
    email: Optional[str] = Field(default=None, description="Búsqueda parcial")
    username: Optional[str] = Field(default=None, description="Búsqueda parcial")
    role: Optional[str] = Field(default=None)
    is_active: Optional[bool] = Field(default=None)
    
    offset: int = Field(default=0, ge=0, description="Número de registros a omitir")
    limit: int = Field(default=20, le=100, description="Máximo 100 registros por consulta para no saturar memoria")

# Response
class UserPublic(UserBase):
    """
    Modelo seguro para devolver al cliente.
    Garantiza la ausencia del campo 'password'.
    """
    id: int
    
    model_config = ConfigDict(from_attributes=True)

# AUTH

class UserLogin(SQLModel):
    """Payload para el endpoint de Login."""
    email: EmailStr
    password: str = Field(max_length=128)

class Token(SQLModel):
    """Payload de respuesta JWT."""
    token: str
    token_type: str