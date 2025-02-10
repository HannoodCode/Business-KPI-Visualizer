import asyncpg
from fastapi import FastAPI
import os

DATABASE_URL = os.getenv("DATABASE_URL")

async def connect_to_db():
    return await asyncpg.create_pool(DATABASE_URL)

async def disconnect_from_db(pool):
    await pool.close()
