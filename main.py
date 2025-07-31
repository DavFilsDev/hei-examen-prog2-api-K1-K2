from fastapi import FastAPI
from fastapi.responses import PlainTextResponse, Response

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