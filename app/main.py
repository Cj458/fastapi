from typing import List
from fastapi import FastAPI

from app.api.vk_api import *
from .routers import user
from .utils import *
from .database import engine
from . import models


models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(user.router)

@app.get("/")
async def root():
    return {"Data": "Hello World"}


