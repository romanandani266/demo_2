from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4
import os
import aiofiles

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
users = {"admin": {"username": "admin", "password": "admin123"}}

class Blog(BaseModel):
    id: str
    title: str
    content: str
    image_url: Optional[str] = None
    created_at: str
    updated_at: str

class UserLogin(BaseModel):
    username: str
    password: str

async def validate_image(file: UploadFile):
    allowed_extensions = {"jpg", "jpeg", "png", "gif"}
    file_extension = file.filename.split(".")[-1].lower()
    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Invalid image format.")
    if file.size > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Image size exceeds 5 MB.")

@app.post("/login")
async def login(user: UserLogin):
    if user.username in users and users[user.username]["password"] == user.password:
        return {"message": "Login successful", "username": user.username}
    raise HTTPException(status_code=401, detail="Invalid username or password.")

@app.get("/blogs")
async def get_blogs():
    return list(blogs.values())

@app.get("/blogs/{blog_id}")
async def get_blog(blog_id: str):
    blog = blogs.get(blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found.")
    return blog

@app.post("/blogs")
async def create_blog(title: str = Form(...), content: str = Form(...), image: Optional[UploadFile] = File(None)):
    blog_id = str(uuid4())
    image_url = None
    if image:
        await validate_image(image)
        image_path = f"images/{blog_id}_{image.filename}"
        os.makedirs("images", exist_ok=True)
        async with aiofiles.open(image_path, "wb") as out_file:
            content = await image.read()
            await out_file.write(content)
        image_url = f"/{image_path}"
    blog = Blog(
        id=blog_id,
        title=title,
        content=content,
        image_url=image_url,
        created_at="2023-01-01T00:00:00Z",
        updated_at="2023-01-01T00:00:00Z"
    )
    blogs[blog_id] = blog.dict()
    return blog

@app.put("/blogs/{blog_id}")
async def update_blog(blog_id: str, title: Optional[str] = Form(None), content: Optional[str] = Form(None), image: Optional[UploadFile] = File(None)):
    blog = blogs.get(blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found.")
    if title:
        blog["title"] = title
    if content:
        blog["content"] = content
    if image:
        await validate_image(image)
        image_path = f"images/{blog_id}_{image.filename}"
        os.makedirs("images", exist_ok=True)
        async with aiofiles.open(image_path, "wb") as out_file:
            content = await image.read()
            await out_file.write(content)
        blog["image_url"] = f"/{image_path}"
    blog["updated_at"] = "2023-01-01T00:00:00Z"
    blogs[blog_id] = blog
    return blog

@app.delete("/blogs/{blog_id}")
async def delete_blog(blog_id: str):
    blog = blogs.pop(blog_id, None)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found.")
    return JSONResponse(content={"message": "Blog deleted successfully."})

@app.get("/images/{image_name}")
async def get_image(image_name: str):
    image_path = f"images/{image_name}"
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found.")
    return FileResponse(image_path)