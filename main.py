from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

class Blog(BaseModel):
    title: str
    body: str
    plublished: Optional[bool]

app = FastAPI()
    
@app.post('/')
def create_blog(blog: Blog):
    return {'data': f'Blog is created with title - {blog.title}'}