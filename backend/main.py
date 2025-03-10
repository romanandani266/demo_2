from fastapi import FastAPI, HTTPException, Query, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4
import pandas as pd
import io

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
users = {}

class Blog(BaseModel):
    title: str
    content: str
    image_url: Optional[str] = None

class BlogResponse(Blog):
    id: str

class User(BaseModel):
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/register", status_code=201)
async def register_user(user: User):
    if user.username in users:
        raise HTTPException(status_code=400, detail="Username already exists")
    users[user.username] = user.password
    return {"message": "User registered successfully"}

@app.post("/login")
async def login_user(login_request: LoginRequest):
    if login_request.username not in users or users[login_request.username] != login_request.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"message": "Login successful"}

@app.get("/blogs", response_model=List[BlogResponse])
async def get_blogs(page: int = Query(1, ge=1), limit: int = Query(10, ge=1)):
    start = (page - 1) * limit
    end = start + limit
    blog_list = list(blogs.values())[start:end]
    return blog_list

@app.get("/blogs/{blog_id}", response_model=BlogResponse)
async def get_blog(blog_id: str):
    blog = blogs.get(blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

@app.post("/blogs", response_model=BlogResponse, status_code=201)
async def create_blog(blog: Blog):
    blog_id = str(uuid4())
    new_blog = BlogResponse(id=blog_id, **blog.dict())
    blogs[blog_id] = new_blog
    return new_blog

@app.put("/blogs/{blog_id}", response_model=BlogResponse)
async def update_blog(blog_id: str, blog: Blog):
    existing_blog = blogs.get(blog_id)
    if not existing_blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    updated_blog = BlogResponse(id=blog_id, **blog.dict())
    blogs[blog_id] = updated_blog
    return updated_blog

@app.delete("/blogs/{blog_id}", status_code=204)
async def delete_blog(blog_id: str):
    if blog_id not in blogs:
        raise HTTPException(status_code=404, detail="Blog not found")
    del blogs[blog_id]
    return

@app.post("/blogs/upload-image")
async def upload_image(file: UploadFile = File(...)):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid image format. Only JPEG and PNG are supported.")
    image_url = f"https://example.com/images/{file.filename}"
    return {"image_url": image_url}

@app.post("/upload-excel")
async def upload_excel(file: UploadFile = File(...)):
    if file.content_type not in ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.ms-excel"]:
        raise HTTPException(status_code=400, detail="Invalid file format. Only Excel files are supported.")
    try:
        content = await file.read()
        df = pd.read_excel(io.BytesIO(content))
        data = df.to_dict(orient="records")
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the Excel file: {str(e)}")