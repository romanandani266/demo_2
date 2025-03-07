from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from datetime import datetime

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

blogs = []
users = {"admin": "password123"}
blog_id_counter = 1

class Blog(BaseModel):
    title: str
    content: str
    image_url: Optional[HttpUrl] = None

class BlogResponse(Blog):
    id: int
    created_at: datetime
    updated_at: datetime

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    message: str
    token: str

@app.get("/blogs", response_model=List[BlogResponse])
async def get_all_blogs():
    return blogs

@app.get("/blogs/{blog_id}", response_model=BlogResponse)
async def get_blog(blog_id: int):
    for blog in blogs:
        if blog["id"] == blog_id:
            return blog
    raise HTTPException(status_code=404, detail="Blog not found")

@app.post("/blogs", response_model=BlogResponse, status_code=201)
async def create_blog(blog: Blog):
    global blog_id_counter
    new_blog = {
        "id": blog_id_counter,
        "title": blog.title,
        "content": blog.content,
        "image_url": blog.image_url,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }
    blogs.append(new_blog)
    blog_id_counter += 1
    return new_blog

@app.put("/blogs/{blog_id}", response_model=BlogResponse)
async def update_blog(blog_id: int, updated_blog: Blog):
    for blog in blogs:
        if blog["id"] == blog_id:
            blog["title"] = updated_blog.title
            blog["content"] = updated_blog.content
            blog["image_url"] = updated_blog.image_url
            blog["updated_at"] = datetime.utcnow()
            return blog
    raise HTTPException(status_code=404, detail="Blog not found")

@app.delete("/blogs/{blog_id}", status_code=204)
async def delete_blog(blog_id: int):
    for blog in blogs:
        if blog["id"] == blog_id:
            blogs.remove(blog)
            return
    raise HTTPException(status_code=404, detail="Blog not found")

@app.post("/login", response_model=LoginResponse)
async def login(login_request: LoginRequest):
    username = login_request.username
    password = login_request.password

    if username in users and users[username] == password:
        return {"message": "Login successful", "token": "fake-jwt-token"}
    raise HTTPException(status_code=401, detail="Invalid username or password")