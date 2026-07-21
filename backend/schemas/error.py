"""Model of ERROR Response.
"""
from pydantic import BaseModel

class Error(BaseModel):
    detail: str