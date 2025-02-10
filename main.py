from fastapi import FastAPI
from database import connect_to_db, disconnect_from_db
from routers import orders

app = FastAPI()

@app.on_event("startup")
async def startup():
    app.state.pool = await connect_to_db()

@app.on_event("shutdown")
async def shutdown():
    await disconnect_from_db(app.state.pool)

app.include_router(orders.router, prefix="/api")
