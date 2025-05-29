#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorClient
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv



load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("MONGO_DB")

@asynccontextmanager
async def lifespan(app: FastAPI):
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    app.state.mongo_client = client
    app.state.db = db
    yield
    client.close()

app = FastAPI(lifespan=lifespan)

# Gestion du chemin absolu pour static

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=STATIC_DIR)

class Event(BaseModel):
    start: int
    stop: Optional[int] = None
    tags: List[str]

def serialize_event(e):
    return {
        "id": str(e["_id"]),
        "start": e["start"],
        "stop": e.get("stop"),
        "tags": e.get("tags", [])
    }

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/add_event")
async def add_event(request: Request, event: Event):
    db = request.app.state.db
    result = await db.events.insert_one(event.model_dump())
    return {"id": str(result.inserted_id)}

@app.get("/list_events")
async def list_events(request: Request):
    db = request.app.state.db
    events = []
    async for e in db.events.find():
        events.append(serialize_event(e))
    return events

@app.delete("/remove_events")
async def remove_events(request: Request, tags: List[str] = Query(...)):
    db = request.app.state.db
    result = await db.events.delete_many({"tags": {"$in": tags}})
    return {"deleted_count": result.deleted_count}
