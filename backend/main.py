from fastapi import FastAPI, HTTPException, Path, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI()

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

blogs = []
users = []
blog_id_counter = 1
user_id_counter = 1

class Blog(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    content: str = Field(..., min_length=10)
    image_url: Optional[str] = Field(None, regex=r"^(http|https)://.*\.(jpg|jpeg|png|gif)$")

class BlogResponse(Blog):
    id: int
    created_at: str
    updated_at: Optional[str] = None

class User(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    message: str
    token: str

def find_blog(blog_id: int):
    for blog in blogs:
        if blog["id"] == blog_id:
            return blog
    return None

def find_user(username: str):
    for user in users:
        if user["username"] == username:
            return user
    return None

@app.post("/register", status_code=201)
async def register_user(user: User):
    global user_id_counter
    if find_user(user.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    new_user = {
        "id": user_id_counter,
        "username": user.username,
        "password": user.password
    }
    users.append(new_user)
    user_id_counter += 1
    return {"message": "User registered successfully"}

@app.post("/login", response_model=LoginResponse)
async def login_user(login_request: LoginRequest):
    user = find_user(login_request.username)
    if not user or user["password"] != login_request.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = f"mock-token-for-{user['username']}"
    return {"message": "Login successful", "token": token}

@app.get("/blogs", response_model=List[BlogResponse])
async def get_blogs():
    return blogs

@app.get("/blogs/{blog_id}", response_model=BlogResponse)
async def get_blog(blog_id: int = Path(...)):
    blog = find_blog(blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

@app.post("/blogs", response_model=BlogResponse, status_code=201)
async def create_blog(blog: Blog):
    global blog_id_counter
    new_blog = {
        "id": blog_id_counter,
        "title": blog.title,
        "content": blog.content,
        "image_url": blog.image_url or "https://plus.unsplash.com/premium_photo-1684581214880-2043e5bc8b8b?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": None
    }
    blogs.append(new_blog)
    blog_id_counter += 1
    return new_blog

@app.put("/blogs/{blog_id}", response_model=BlogResponse)
async def update_blog(blog_id: int = Path(...), updated_blog: Blog = Body(...)):
    blog = find_blog(blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    blog["title"] = updated_blog.title
    blog["content"] = updated_blog.content
    blog["image_url"] = updated_blog.image_url or blog["image_url"]
    blog["updated_at"] = "2023-01-02T00:00:00Z"
    return blog

@app.delete("/blogs/{blog_id}", status_code=204)
async def delete_blog(blog_id: int = Path(...)):
    global blogs
    blog = find_blog(blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    blogs = [b for b in blogs if b["id"] != blog_id]
    return None