from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from uuid import uuid4
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

blogs = {}
users = {"admin": {"username": "admin", "password": "admin123"}}

class BlogBase(BaseModel):
    title: str
    content: str
    image_url: Optional[HttpUrl] = None

class BlogCreate(BlogBase):
    pass

class BlogUpdate(BlogBase):
    pass

class BlogResponse(BlogBase):
    id: str
    created_at: datetime
    updated_at: datetime

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    message: str
    token: str

@app.get("/blogs", response_model=List[BlogResponse])
async def get_blogs():
    return list(blogs.values())

@app.get("/blogs/{blog_id}", response_model=BlogResponse)
async def get_blog(blog_id: str):
    blog = blogs.get(blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

@app.post("/blogs", response_model=BlogResponse)
async def create_blog(
    title: str = Form(...),
    content: str = Form(...),
    image: Optional[UploadFile] = File(None)
):
    blog_id = str(uuid4())
    created_at = datetime.utcnow()
    updated_at = created_at

    image_url = None
    if image:
        if image.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(status_code=400, detail="Invalid image format. Only JPEG and PNG are allowed.")
        image_url = f"https://example.com/images/{image.filename}"

    blog = {
        "id": blog_id,
        "title": title,
        "content": content,
        "image_url": image_url,
        "created_at": created_at,
        "updated_at": updated_at,
    }
    blogs[blog_id] = blog
    return blog

@app.put("/blogs/{blog_id}", response_model=BlogResponse)
async def update_blog(
    blog_id: str,
    title: str = Form(...),
    content: str = Form(...),
    image: Optional[UploadFile] = File(None)
):
    blog = blogs.get(blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    image_url = blog["image_url"]
    if image:
        if image.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(status_code=400, detail="Invalid image format. Only JPEG and PNG are allowed.")
        image_url = f"https://example.com/images/{image.filename}"

    updated_at = datetime.utcnow()
    blog.update({
        "title": title,
        "content": content,
        "image_url": image_url,
        "updated_at": updated_at,
    })
    return blog

@app.delete("/blogs/{blog_id}")
async def delete_blog(blog_id: str):
    blog = blogs.pop(blog_id, None)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return {"message": "Blog deleted successfully"}

@app.post("/login", response_model=LoginResponse)
async def login(login_request: LoginRequest):
    user = users.get(login_request.username)
    if not user or user["password"] != login_request.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = f"token-{uuid4()}"
    return {"message": "Login successful", "token": token}