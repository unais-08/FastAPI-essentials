from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.connection import create_db_pool
from app.routes import blog


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting up...")
    app.state.db_pool = await create_db_pool()
    yield
    print("🛑 Shutting down...")
    await app.state.db_pool.close()


app = FastAPI(lifespan=lifespan)


@app.get("/")
def index():
    return {"message": "hello from FastAPI"}


app.include_router(blog.router)
