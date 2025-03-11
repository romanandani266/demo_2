from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

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

class User(BaseModel):
    username: str
    password: str
    role: str

class Product(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float

class Location(BaseModel):
    id: int
    name: str
    address: Optional[str]

class Inventory(BaseModel):
    product_id: int
    location_id: int
    stock_level: int

class Sale(BaseModel):
    product_id: int
    location_id: int
    quantity: int
    timestamp: str

class RestockingAlert(BaseModel):
    product_id: int
    location_id: int
    stock_level: int
    threshold: int

users = [
    {"username": "admin", "password": "admin123", "role": "admin"},
    {"username": "manager1", "password": "manager123", "role": "store_manager"},
]

products = [
    {"id": 1, "name": "Product A", "description": "Description A", "price": 10.0},
    {"id": 2, "name": "Product B", "description": "Description B", "price": 20.0},
]

locations = [
    {"id": 1, "name": "Warehouse 1", "address": "123 Main St"},
    {"id": 2, "name": "Store 1", "address": "456 Elm St"},
]

inventory = [
    {"product_id": 1, "location_id": 1, "stock_level": 100},
    {"product_id": 2, "location_id": 2, "stock_level": 50},
]

sales = [
    {"product_id": 1, "location_id": 1, "quantity": 10, "timestamp": "2023-10-01T10:00:00"},
    {"product_id": 2, "location_id": 2, "quantity": 5, "timestamp": "2023-10-01T11:00:00"},
]

alerts = [
    {"product_id": 1, "location_id": 1, "stock_level": 10, "threshold": 20},
]

def authenticate_user(username: str, password: str):
    user = next((u for u in users if u["username"] == username and u["password"] == password), None)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

@app.post("/api/auth/login")
def login(data: User):
    user = authenticate_user(data.username, data.password)
    return {"message": f"Welcome {user['username']}!", "role": user["role"]}

@app.get("/api/inventory", response_model=List[Inventory])
def get_inventory():
    return inventory

@app.put("/api/inventory")
def update_inventory(product_id: int, location_id: int, stock_level: int):
    item = next((i for i in inventory if i["product_id"] == product_id and i["location_id"] == location_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    item["stock_level"] = stock_level
    return {"message": "Inventory updated successfully", "inventory": item}

@app.get("/api/alerts", response_model=List[RestockingAlert])
def get_alerts():
    return alerts

@app.get("/api/sales-trends", response_model=List[Sale])
def get_sales_trends():
    return sales

@app.post("/api/users")
def create_user(user: User):
    if any(u["username"] == user.username for u in users):
        raise HTTPException(status_code=400, detail="User already exists")
    users.append(user.dict())
    return {"message": "User created successfully", "user": user}

@app.get("/api/products", response_model=List[Product])
def get_products():
    return products

@app.post("/api/products")
def create_product(product: Product):
    if any(p["id"] == product.id for p in products):
        raise HTTPException(status_code=400, detail="Product with this ID already exists")
    products.append(product.dict())
    return {"message": "Product created successfully", "product": product}

@app.get("/api/locations", response_model=List[Location])
def get_locations():
    return locations

@app.post("/api/locations")
def create_location(location: Location):
    if any(l["id"] == location.id for l in locations):
        raise HTTPException(status_code=400, detail="Location with this ID already exists")
    locations.append(location.dict())
    return {"message": "Location created successfully", "location": location}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
