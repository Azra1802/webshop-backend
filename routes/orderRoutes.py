import json
from pathlib import Path
from fastapi import APIRouter, HTTPException, Query
from typing import List, Literal
from datetime import datetime

from models.orderModel import Order, OrderCreate

router = APIRouter()
ORDERS_FILE = Path("orders.json")

def load_orders() -> List[Order]:
    if ORDERS_FILE.exists():
        with open(ORDERS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Order(**item) for item in data]
    return []

def save_orders(orders: List[Order]):
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump([order.dict() for order in orders], f, default=str, indent=4)

@router.get("/", response_model=List[Order])
def get_orders():
    return load_orders()

@router.get("/{id}", response_model=Order)
def get_order(id: int):
    orders = load_orders()
    for order in orders:
        if order.id == id:
            return order
    raise HTTPException(status_code=404, detail="Order not found")    

@router.post("/", status_code=201)
def create_order(order_data: OrderCreate):
    orders = load_orders()
    new_id = max([o.id for o in orders], default=0) + 1

    new_order = Order(
        id=new_id,
        name=order_data.name,
        email=order_data.email,
        address=order_data.address,
        items=order_data.items,
        total_price=order_data.total_price,
        status="pending",  # default, ali možeš i izostaviti jer je već zadano
        created_at=datetime.utcnow()
    )

    orders.append(new_order)
    save_orders(orders)
    return {"message": "Order placed successfully", "order_id": new_id}

@router.put("/{order_id}/status")
def update_order_status(
    order_id: int,
    new_status: Literal["pending", "accepted", "completed", "rejected"] = Query(...)
):
    orders = load_orders()
    for order in orders:
        if order.id == order_id:
            order.status = new_status
            save_orders(orders)
            return {"message": "Status updated"}
    raise HTTPException(status_code=404, detail="Order not found")
