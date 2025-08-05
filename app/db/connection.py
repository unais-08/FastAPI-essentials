import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()


# We'll no longer use a global variable here.
async def create_db_pool():
    return await asyncpg.create_pool(dsn=os.getenv("DATABASE_URL"))
