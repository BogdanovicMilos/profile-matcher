from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from application.api.routers import client, player
from application.config.settings import settings
from utils.player_initializer import init_player


VERSION = "0.1.0"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Insert initial Player data into the database
    await init_player()
    yield


app = FastAPI(title="Profile Matcher API", version=VERSION, lifespan=lifespan)

origins = settings.allowed_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(client.router)
app.include_router(player.router)


@app.get("/healthcheck", operation_id="health_check")
async def health_check():
    return {"message": "Ok"}
