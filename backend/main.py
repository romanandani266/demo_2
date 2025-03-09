from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://yourfrontend.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mock_inventory = [
    {"product_id": 1, "location_id": 1, "stock_level": 50},
    {"product_id": 2, "location_id": 1, "stock_level": 20},
]
mock_sales = [
    {"product_id": 1, "location_id": 1, "sales_data": [10, 15, 20]},
    {"product_id": 2, "location_id": 1, "sales_data": [5, 7, 8]},
]
mock_users = [
    {"user_id": 1, "username": "admin", "password": "admin123", "role": "admin"},
    {"user_id": 2, "username": "manager", "password": "manager123", "role": "manager"},
]

class InventoryItem(BaseModel):
    product_id: int
    location_id: int
    stock_level: int

class SalesTrend(BaseModel):
    product_id: int
    location_id: int
    sales_data: List[int]

class RestockingAlert(BaseModel):
    product_id: int
    location_id: int
    message: str

class User(BaseModel):
    user_id: int
    username: str
    role: str

class AuthRequest(BaseModel):
    username: str
    password: str

class AuthResponse(BaseModel):
    access_token: str
    token_type: str

@app.get("/api/inventory", response_model=List[InventoryItem])
def get_inventory():
    return mock_inventory

@app.put("/api/inventory", response_model=InventoryItem)
def update_inventory(item: InventoryItem):
    for inventory_item in mock_inventory:
        if inventory_item["product_id"] == item.product_id and inventory_item["location_id"] == item.location_id:
            inventory_item["stock_level"] = item.stock_level
            return inventory_item
    raise HTTPException(status_code=404, detail="Inventory item not found")

@app.get("/api/alerts", response_model=List[RestockingAlert])
def get_restocking_alerts():
    alerts = []
    for inventory_item in mock_inventory:
        if inventory_item["stock_level"] < 10:
            alerts.append(
                RestockingAlert(
                    product_id=inventory_item["product_id"],
                    location_id=inventory_item["location_id"],
                    message="Stock is below the threshold. Restocking required.",
                )
            )
    return alerts

@app.get("/api/sales-trends", response_model=List[SalesTrend])
def get_sales_trends():
    return mock_sales

@app.post("/api/auth/login", response_model=AuthResponse)
def login(auth_request: AuthRequest):
    user = next((user for user in mock_users if user["username"] == auth_request.username), None)
    if not user or user["password"] != auth_request.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"access_token": user["username"], "token_type": "bearer"}

@app.post("/api/users", response_model=User)
def create_user(user: User):
    existing_user = next((u for u in mock_users if u["username"] == user.username), None)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    mock_users.append(user.dict())
    return user