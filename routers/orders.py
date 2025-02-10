from fastapi import APIRouter, Depends
from database import connect_to_db

router = APIRouter()

@router.get("/orders")
async def get_orders(limit: int = 10, pool=Depends(connect_to_db)):
    async with pool.acquire() as connection:
        rows = await connection.fetch("SELECT * FROM orders LIMIT $1", limit)
        return [dict(row) for row in rows]
