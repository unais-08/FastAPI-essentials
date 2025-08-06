from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.connection import create_db_pool
from app.routes import blog, user
from fastapi.middleware.cors import CORSMiddleware

# Allow all origins (you can restrict this in production)
origins = [
    "http://localhost:5173",  # React dev server
    "http://127.0.0.1:5173",
    "https://your-frontend-domain.com",  # production frontend
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting up...")
    app.state.db_pool = await create_db_pool()
    yield
    print("🛑 Shutting down...")
    await app.state.db_pool.close()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # allows these origins
    allow_credentials=True,
    allow_methods=["*"],  # allows all methods like GET, POST, PUT, DELETE
    allow_headers=["*"],  # allows all headers
)


@app.get("/")
def index():
    return {"message": "hello from FastAPI"}


app.include_router(user.router)
app.include_router(blog.router)
