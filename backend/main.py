from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Retail Inventory Management System", version="1.0.0")

origins = [
    "http://localhost:3000",
    "https://yourfrontend.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

mock_inventory = [
    {"product_id": 1, "location_id": 1, "stock_level": 50},
    {"product_id": 2, "location_id": 1, "stock_level": 20}
]
mock_sales = [
    {"product_id": 1, "quantity_sold": 10, "date": "2023-10-01"},
    {"product_id": 2, "quantity_sold": 5, "date": "2023-10-01"}
]
mock_alerts = [
    {"product_id": 2, "location_id": 1, "alert_message": "Low stock: Restock needed"}
]
mock_users = [
    {"username": "admin", "password": "admin123", "role": "admin"},
    {"username": "manager", "password": "manager123", "role": "manager"}
]

class InventoryItem(BaseModel):
    product_id: int
    location_id: int
    stock_level: int

class SalesData(BaseModel):
    product_id: int
    quantity_sold: int
    date: str

class RestockingAlert(BaseModel):
    product_id: int
    location_id: int
    alert_message: str

class User(BaseModel):
    username: str
    role: str

class LoginRequest(BaseModel):
    username: str
    password: str

def get_current_user(token: str) -> User:
    user = next((user for user in mock_users if user["username"] == token), None)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return User(username=user["username"], role=user["role"])

@app.get("/api/inventory", response_model=List[InventoryItem])
def get_inventory(token: str):
    get_current_user(token)
    return mock_inventory

@app.put("/api/inventory", response_model=InventoryItem)
def update_inventory(item: InventoryItem, token: str):
    get_current_user(token)
    for inventory_item in mock_inventory:
        if inventory_item["product_id"] == item.product_id and inventory_item["location_id"] == item.location_id:
            inventory_item["stock_level"] = item.stock_level
            return inventory_item
    raise HTTPException(status_code=404, detail="Inventory item not found")

@app.get("/api/alerts", response_model=List[RestockingAlert])
def get_restocking_alerts(token: str):
    get_current_user(token)
    return mock_alerts

@app.get("/api/sales-trends", response_model=List[SalesData])
def get_sales_trends(token: str):
    get_current_user(token)
    return mock_sales

@app.post("/api/auth/login")
def login(login_request: LoginRequest):
    user = next((user for user in mock_users if user["username"] == login_request.username), None)
    if not user or user["password"] != login_request.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"access_token": user["username"], "token_type": "bearer"}

@app.post("/api/users", response_model=User)
def create_user(user: User, token: str):
    current_user = get_current_user(token)
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to create users")
    mock_users.append({"username": user.username, "password": "default", "role": user.role})
    return user

@app.get("/")
def root():
    return {"message": "Welcome to the Retail Inventory Management System API"}