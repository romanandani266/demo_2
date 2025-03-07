from fastapi import FastAPI, HTTPException, Path, Body, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from datetime import datetime
import uuid
import imghdr

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

blogs = {}
users = {"admin": {"password": "admin123"}}

class BlogBase(BaseModel):
    title: str
    content: str
    image_url: Optional[HttpUrl] = None

class BlogCreate(BlogBase):
    pass

class BlogUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    image_url: Optional[HttpUrl] = None

class BlogResponse(BlogBase):
    id: str
    created_at: datetime

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    message: str
    token: Optional[str] = None

def validate_image(file: UploadFile):
    valid_image_types = ["jpeg", "png", "gif"]
    file_type = imghdr.what(file.file)
    if file_type not in valid_image_types:
        raise HTTPException(status_code=400, detail="Invalid image format. Only JPEG, PNG, and GIF are allowed.")
    return True

@app.get("/blogs", response_model=List[BlogResponse])
async def get_blogs():
    return list(blogs.values())

@app.get("/blogs/{blog_id}", response_model=BlogResponse)
async def get_blog(blog_id: str = Path(...)):
    blog = blogs.get(blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return blog

@app.post("/blogs", response_model=BlogResponse)
async def create_blog(blog: BlogCreate = Body(...)):
    blog_id = str(uuid.uuid4())
    new_blog = {
        "id": blog_id,
        "title": blog.title,
        "content": blog.content,
        "image_url": blog.image_url,
        "created_at": datetime.utcnow()
    }
    blogs[blog_id] = new_blog
    return new_blog

@app.put("/blogs/{blog_id}", response_model=BlogResponse)
async def update_blog(blog_id: str = Path(...), blog_update: BlogUpdate = Body(...)):
    blog = blogs.get(blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog post not found")
    if blog_update.title is not None:
        blog["title"] = blog_update.title
    if blog_update.content is not None:
        blog["content"] = blog_update.content
    if blog_update.image_url is not None:
        blog["image_url"] = blog_update.image_url
    blogs[blog_id] = blog
    return blog

@app.delete("/blogs/{blog_id}")
async def delete_blog(blog_id: str = Path(...)):
    if blog_id not in blogs:
        raise HTTPException(status_code=404, detail="Blog post not found")
    del blogs[blog_id]
    return {"message": "Blog post deleted successfully"}

@app.post("/blogs/upload-image")
async def upload_image(file: UploadFile = File(...)):
    validate_image(file)
    return {"message": "Image uploaded successfully"}

@app.post("/login", response_model=LoginResponse)
async def login(login_request: LoginRequest = Body(...)):
    user = users.get(login_request.username)
    if not user or user["password"] != login_request.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"message": "Login successful", "token": "dummy_token"}

@app.get("/")
async def root():
    return {"message": "Welcome to the Modern Blog Platform API"}