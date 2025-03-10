from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid

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
    allow_headers=["*"],
)

blogs = {}
users = {"admin": {"username": "admin", "password": "admin123"}}

class Blog(BaseModel):
    id: str
    title: str
    content: str
    image_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class BlogCreate(BaseModel):
    title: str
    content: str
    image_url: Optional[str] = None

class BlogUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    image_url: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    message: str
    token: str

@app.get("/blogs", response_model=List[Blog])
def get_all_blogs():
    return list(blogs.values())

@app.get("/blogs/{blog_id}", response_model=Blog)
def get_blog(blog_id: str):
    if blog_id not in blogs:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blogs[blog_id]

@app.post("/blogs", response_model=Blog, status_code=201)
def create_blog(blog: BlogCreate):
    blog_id = str(uuid.uuid4())
    new_blog = Blog(
        id=blog_id,
        title=blog.title,
        content=blog.content,
        image_url=blog.image_url,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    blogs[blog_id] = new_blog
    return new_blog

@app.put("/blogs/{blog_id}", response_model=Blog)
def update_blog(blog_id: str, blog_update: BlogUpdate):
    if blog_id not in blogs:
        raise HTTPException(status_code=404, detail="Blog not found")
    existing_blog = blogs[blog_id]
    updated_blog = existing_blog.copy(update=blog_update.dict(exclude_unset=True))
    updated_blog.updated_at = datetime.utcnow()
    blogs[blog_id] = updated_blog
    return updated_blog

@app.delete("/blogs/{blog_id}", status_code=204)
def delete_blog(blog_id: str):
    if blog_id not in blogs:
        raise HTTPException(status_code=404, detail="Blog not found")
    del blogs[blog_id]
    return {"message": "Blog deleted successfully"}

@app.post("/blogs/upload-image")
def upload_image(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only images are allowed.")
    image_url = f"https://example.com/images/{file.filename}"
    return {"image_url": image_url}

@app.post("/login", response_model=LoginResponse)
def login(login_request: LoginRequest):
    username = login_request.username
    password = login_request.password
    if username not in users or users[username]["password"] != password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = f"fake-token-for-{username}"
    return {"message": "Login successful", "token": token}