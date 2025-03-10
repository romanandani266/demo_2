from fastapi import FastAPI, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from datetime import datetime

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

class BlogBase(BaseModel):
    title: str
    content: str
    image_url: Optional[HttpUrl] = None

class BlogCreate(BlogBase):
    pass

class BlogUpdate(BlogBase):
    title: Optional[str] = None
    content: Optional[str] = None
    image_url: Optional[HttpUrl] = None

class Blog(BlogBase):
    id: int
    created_at: datetime
    updated_at: datetime

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str

blogs = []
users = {"admin": "password123"}
blog_id_counter = 1

@app.get("/blogs", response_model=List[Blog])
async def get_all_blogs():
    return blogs

@app.get("/blogs/{blog_id}", response_model=Blog)
async def get_blog(blog_id: int):
    for blog in blogs:
        if blog["id"] == blog_id:
            return blog
    raise HTTPException(status_code=404, detail="Blog not found")

@app.post("/blogs", response_model=Blog, status_code=201)
async def create_blog(blog: BlogCreate):
    global blog_id_counter
    new_blog = {
        "id": blog_id_counter,
        "title": blog.title,
        "content": blog.content,
        "image_url": blog.image_url,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    blogs.append(new_blog)
    blog_id_counter += 1
    return new_blog

@app.put("/blogs/{blog_id}", response_model=Blog)
async def update_blog(blog_id: int, blog_update: BlogUpdate):
    for blog in blogs:
        if blog["id"] == blog_id:
            if blog_update.title is not None:
                blog["title"] = blog_update.title
            if blog_update.content is not None:
                blog["content"] = blog_update.content
            if blog_update.image_url is not None:
                blog["image_url"] = blog_update.image_url
            blog["updated_at"] = datetime.now()
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
    if login_request.username in users and users[login_request.username] == login_request.password:
        return {"access_token": "fake-jwt-token", "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid username or password")