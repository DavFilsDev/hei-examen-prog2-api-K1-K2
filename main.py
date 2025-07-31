from fastapi import FastAPI
from fastapi.responses import PlainTextResponse, Response
from pydantic import BaseModel
from datetime import datetime
from typing import List


app = FastAPI()

@app.get("/ping", response_class=PlainTextResponse)
def ping():
    return "pong"

@app.get("/home")
def hello():
    with open("home.html", "r", encoding="utf-8") as file:
        html_content = file.read()

    return Response(
        content=html_content,
        status_code=200,
        media_type="text/html"
    )

@app.get("/{full_path:path}")
def catch_all(full_path: str):
    with open("404.html", "r", encoding="utf-8") as file:
        html_content = file.read()

    return Response(
        content=html_content,
        status_code=404,
        media_type="text/html"
    )

class PostModel(BaseModel):
    author: str
    title: str
    content: str
    creation_datetime: datetime

posts_store: List[PostModel] = []

def serialize_posts():
    return [post.model_dump() for post in posts_store]

@app.post("/posts", status_code=201)
def create_posts(new_posts: List[PostModel]):
    posts_store.extend(new_posts)
    return serialize_posts()