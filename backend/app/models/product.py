from pydantic import BaseModel
from typing import Optional
import strawberry

class ProductCreate(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    stock: int = 0
    category: Optional[str] = None

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    stock: Optional[int] = None
    category: Optional[str] = None

class Product(BaseModel):
    id: int
    name: str
    price: float
    description: Optional[str] = None
    stock: int = 0
    category: Optional[str] = None
    is_active: bool = True

@strawberry.type
class ProductType:
    id: int
    name: str
    price: float
    description: Optional[str] = None
    stock: int
    category: Optional[str] = None
    is_active: bool

@strawberry.input
class ProductInput:
    name: str
    price: float
    description: Optional[str] = None
    stock: int = 0
    category: Optional[str] = None

@strawberry.input
class ProductUpdateInput:
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    stock: Optional[int] = None
    category: Optional[str] = None