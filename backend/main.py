from fastapi import FastAPI, HTTPException, Path, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import List

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

class Blog(BaseModel):
    id: int
    title: str
    content: str
    image_url: HttpUrl
    created_at: datetime

class BlogCreate(BaseModel):
    title: str
    content: str
    image_url: HttpUrl

class BlogUpdate(BaseModel):
    title: str
    content: str
    image_url: HttpUrl

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str

blogs = []
blog_id_counter = 1

users = {
    "testuser": "password123"
}

@app.get("/blogs", response_model=List[Blog])
def get_all_blogs():
    return blogs

@app.get("/blogs/{blog_id}", response_model=Blog)
def get_blog(blog_id: int = Path(...)):
    for blog in blogs:
        if blog.id == blog_id:
            return blog
    raise HTTPException(status_code=404, detail="Blog not found")

@app.post("/blogs", response_model=Blog, status_code=201)
def create_blog(blog: BlogCreate = Body(...)):
    global blog_id_counter
    new_blog = Blog(
        id=blog_id_counter,
        title=blog.title,
        content=blog.content,
        image_url=blog.image_url,
        created_at=datetime.now()
    )
    blogs.append(new_blog)
    blog_id_counter += 1
    return new_blog

@app.put("/blogs/{blog_id}", response_model=Blog)
def update_blog(blog_id: int = Path(...), updated_blog: BlogUpdate = Body(...)):
    for index, blog in enumerate(blogs):
        if blog.id == blog_id:
            blogs[index] = Blog(
                id=blog_id,
                title=updated_blog.title,
                content=updated_blog.content,
                image_url=updated_blog.image_url,
                created_at=blog.created_at
            )
            return blogs[index]
    raise HTTPException(status_code=404, detail="Blog not found")

@app.delete("/blogs/{blog_id}", status_code=204)
def delete_blog(blog_id: int = Path(...)):
    for index, blog in enumerate(blogs):
        if blog.id == blog_id:
            blogs.pop(index)
            return
    raise HTTPException(status_code=404, detail="Blog not found")

@app.post("/login", response_model=LoginResponse)
def login(login_request: LoginRequest = Body(...)):
    if login_request.username in users and users[login_request.username] == login_request.password:
        return LoginResponse(access_token="fake-jwt-token", token_type="bearer")
    raise HTTPException(status_code=401, detail="Invalid username or password")