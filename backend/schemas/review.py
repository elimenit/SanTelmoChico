"""Modelos acerca de las estrellas.
"""
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel

class ReviewBase(SQLModel):
    stars: Optional[int] = Field(default=None, ge=1, le=5)
    description: Optional[str] = Field(default=None)

# BD
class Review(ReviewBase, table=True):
    __tablename__ = "reviews"

    id: Optional[int] = Field(default=None, primary_key=True)
    
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    
    user: Optional["User"] = Relationship(back_populates="reviews")

# Request
class ReviewUpsert(BaseModel):
    id: int = Field(gt=0, lt=1_000_000)

class ReviewCreate(ReviewBase):
    stars: int = Field(ge=1, le=5) 
    description: str

class ReviewUpdate(ReviewBase):
    id: int
    stars: int 
    description: str  

class ReviewDelete(BaseModel):
    id: int = Field(gt=0, lt=100_000)

class ReviewFilters(BaseModel):
    stars: Optional[int] = None 

# Response
class ReviewPublic(ReviewBase):
    id: int 
    user_id: int 