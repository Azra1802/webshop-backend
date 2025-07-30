from pydantic import BaseModel, Field, EmailStr
from typing import List, Literal
from datetime import datetime

class OrderItem(BaseModel):
    id: int
    name: str
    quantity: int
    price: float
    image_url: str

class OrderCreate(BaseModel):
    name: str = Field(..., example="John Doe")
    email: EmailStr
    address: str
    items: List[OrderItem]
    total_price: float

class Order(OrderCreate):
    id: int
    status: Literal["pending", "accepted", "completed", "rejected"] = "pending"
    created_at: datetime = Field(default_factory=datetime.utcnow)
