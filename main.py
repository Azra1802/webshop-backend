import json
from pathlib import Path
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from routes.orderRoutes import router as order_router

app = FastAPI()


origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://webshop-frontend-amber.vercel.app/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],   
    allow_headers=["*"],   
)

DATA_FILE = Path("products.json")


class ProductCreate(BaseModel):
    name: str = Field(..., example="Sample Product")
    description: Optional[str] = Field(None, example="Basic product description")
    price: float = Field(..., gt=0, example=9.99)
    image_url: Optional[str] = Field(None, example="http://example.com/image.jpg")
    quantity: int = Field(..., ge=0, example=50)

class Product(ProductCreate):
    id: int
    publish_date: datetime = Field(default_factory=datetime.utcnow)

class PasswordChangeRequest(BaseModel):
    username: str = Field(..., example="admin")
    current_password: str = Field(..., example="password123")
    new_password: str = Field(..., min_length=6, example="newsecurepassword")

def load_products() -> List[Product]:
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Product(**item) for item in data]
    return []

def save_products(products: List[Product]) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([p.dict() for p in products], f, default=str, indent=4)

ADMIN_FILE = Path("admin.json")

def load_admin_data():
    if ADMIN_FILE.exists():
        with open(ADMIN_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def save_admin_data(data):
    with open(ADMIN_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

@app.get("/products", response_model=List[Product])
def get_products():
    return load_products()

@app.get("/products/{id}", response_model=Product)
def get_product(id: int):
    products = load_products()
    for product in products:
        if product.id == id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")

@app.post("/products")
def add_product(product_data: ProductCreate):
    products = load_products()
    new_id = max([p.id for p in products], default=0) + 1

    new_product = Product(
        id=new_id,
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
        image_url=product_data.image_url,
        quantity=product_data.quantity,
        publish_date=datetime.utcnow()
    )
    products.append(new_product)
    save_products(products)
    return {"message": "Product added", "product_id": new_id}

@app.put("/products/{id}")
def update_product(id: int, updated_product: Product):
    products = load_products()
    for i, product in enumerate(products):
        if product.id == id:
            products[i] = updated_product
            save_products(products)
            return {"message": "Product updated"}
    raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/products/{id}")
def delete_product(id: int):
    products = load_products()
    for i, product in enumerate(products):
        if product.id == id:
            products.pop(i)
            save_products(products)
            return {"message": "Product deleted"}
    raise HTTPException(status_code=404, detail="Product not found")

@app.put("/admin/change-password")
def change_password(payload: PasswordChangeRequest = Body(...)):
    admin = load_admin_data()
    if not admin:
        raise HTTPException(status_code=500, detail="Admin data not found.")

    if payload.username != admin.get("username"):
        raise HTTPException(status_code=400, detail="Invalid username.")

    if payload.current_password != admin.get("password"):
        raise HTTPException(status_code=400, detail="Current password is incorrect.")

    admin["password"] = payload.new_password
    save_admin_data(admin)
    return {"message": "Password changed successfully."}

@app.post("/admin/login")
def admin_login(data: dict = Body(...)):
    username = data.get("username")
    password = data.get("password")

    admin = load_admin_data()
    if not admin:
        raise HTTPException(status_code=500, detail="Admin data not configured.")

    admin_username = admin.get("username")
    admin_password = admin.get("password")

    if username == admin_username and password == admin_password:
        return {"token": "dummy-token-123"}
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")    

app.include_router(order_router, prefix="/orders")
