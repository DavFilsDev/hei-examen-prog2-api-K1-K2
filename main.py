from fastapi import FastAPI, Request
from starlette.responses import JSONResponse
from pydantic import BaseModel
from typing import List

app = FastAPI()

