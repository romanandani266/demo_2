from fastapi import FastAPI, HTTPException, Path, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl, Field
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
    title: str = Field(..., max_length=255)
    content: str = Field(...)
    image_url: HttpUrl = Field(...)

class BlogCreate(BlogBase):
    pass

class BlogUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    content: Optional[str] = Field(None)
    image_url: Optional[HttpUrl] = Field(None)

class Blog(BlogBase):
    id: int
    created_at: datetime

class UserLogin(BaseModel):
    username: str
    password: str

blogs = []
blog_id_counter = 1
users = {"admin": "password123"}

@app.get("/blogs", response_model=List[Blog])
def get_all_blogs():
    return blogs

@app.get("/blogs/{blog_id}", response_model=Blog)
def get_blog(blog_id: int = Path(...)):
    for blog in blogs:
        if blog.id == blog_id:
            return blog
    raise HTTPException(status_code=404, detail="Blog post not found")

@app.post("/blogs", response_model=Blog, status_code=201)
def create_blog(blog: BlogCreate):
    global blog_id_counter
    new_blog = Blog(
        id=blog_id_counter,
        title=blog.title,
        content=blog.content,
        image_url=blog.image_url,
        created_at=datetime.utcnow()
    )
    blogs.append(new_blog)
    blog_id_counter += 1
    return new_blog

@app.put("/blogs/{blog_id}", response_model=Blog)
def update_blog(blog_id: int = Path(...), blog_update: BlogUpdate = Body(...)):
    for blog in blogs:
        if blog.id == blog_id:
            if blog_update.title is not None:
                blog.title = blog_update.title
            if blog_update.content is not None:
                blog.content = blog_update.content
            if blog_update.image_url is not None:
                blog.image_url = blog_update.image_url
            return blog
    raise HTTPException(status_code=404, detail="Blog post not found")

@app.delete("/blogs/{blog_id}", status_code=204)
def delete_blog(blog_id: int = Path(...)):
    global blogs
    for blog in blogs:
        if blog.id == blog_id:
            blogs = [b for b in blogs if b.id != blog_id]
            return
    raise HTTPException(status_code=404, detail="Blog post not found")

@app.post("/login")
def login(user: UserLogin):
    if user.username in users and users[user.username] == user.password:
        return {"message": "Login successful", "username": user.username}
    raise HTTPException(status_code=401, detail="Invalid username or password")