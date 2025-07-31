from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.responses import PlainTextResponse, Response
from pydantic import BaseModel
from datetime import datetime
from typing import List
from fastapi.exception_handlers import http_exception_handler
from starlette.exceptions import HTTPException as StarletteHTTPException


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

@app.exception_handler(StarletteHTTPException)
async def custom_404_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        with open("404.html", "r", encoding="utf-8") as file:
            html_content = file.read()

        return HTMLResponse(
            content=html_content,
            status_code=404
        )
    return await http_exception_handler(request, exc)

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

@app.get("/posts")
def get_posts():
    return serialize_posts()