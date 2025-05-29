#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import List

import pytest
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient

from app.main import app
from httpx import AsyncClient


load_dotenv()


app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent.parent
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

MONGO_DB_TEST="http://localhost:27017/event_db_test?authSource=admin"

# Use different DB name for testing to avoid data loss
#MONGO_URL = os.getenv("MONGO_URL") 
DB_TEST = os.getenv("MONGO_DB_TEST")  

@asynccontextmanager
async def lifespan(app: FastAPI):
    client = AsyncIOMotorClient(MONGO_DB_TEST)
    db = client[DB_TEST]
    app.state.mongo_client = client
    app.state.db = db
    yield
    client.close()


client = TestClient(app)

# Ajout d'un événement
@pytest.mark.asyncio
async def test_add():
    async with AsyncClient(base_url=MONGO_DB_TEST) as ac:   
        payload = {"start": 1234567890, "stop": 1234567999, "tags": ["test", "pytest"]}
        resp = ac.post("/add_event", json=payload)
        assert resp
 
# Liste des événements
@pytest.mark.asyncio
async def test_list_events():
    async with AsyncClient(base_url=MONGO_DB_TEST) as ac:
        response = ac.get("/list_events", params={"tag": "*"})
        events = response
        assert events

# Ajout d'un événement à supprimer
@pytest.mark.asyncio
async def test_remove_event():
    async with AsyncClient(base_url=MONGO_DB_TEST) as ac:
        payload = {"start": 987654321, "tags": ["toremove"]}
        # Ajout d'un événement
        ac.post("/add_event", json=payload)
        # Suppression
        resp = client.delete("/remove_events", params={"tags": "toremove"})
        assert resp


