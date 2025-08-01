from fastapi import FastAPI
from fastapi import Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.responses import PlainTextResponse, Response
from pydantic import BaseModel
from datetime import datetime
from typing import List
from fastapi.exception_handlers import http_exception_handler
from starlette.exceptions import HTTPException as StarletteHTTPException
import base64

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

@app.put("/posts")
def update_or_add_post(post: PostModel):
    for i, stored in enumerate(posts_store):
        if stored.title == post.title:
            if stored != post:
                posts_store[i] = post
                return {"status": f"{post.title} updated"}
            else:
                return {"status": f"{post.title} already up-to-date"}
    posts_store.append(post)
    return {"status": f"{post.title} added"}

def decode_basic_auth(auth_header: str):
    if not auth_header.startswith("Basic "):
        raise HTTPException(status_code=400, detail="Invalid auth header format")

    encoded = auth_header.split(" ")[1]
    try:
        decoded = base64.b64decode(encoded).decode("utf-8")
        username, password = decoded.split(":", 1)
        return username, password
    except Exception:
        raise HTTPException(status_code=400, detail="Unable to decode credentials")

@app.get("/ping/auth", response_class=PlainTextResponse)
def ping_auth(request: Request):
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    username, password = decode_basic_auth(auth_header)

    if username == "admin" and password == "123456":
        return "pong"

    raise HTTPException(status_code=403, detail="Invalid credentials")
