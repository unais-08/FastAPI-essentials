import asyncio
import asyncpg
import os
from dotenv import load_dotenv
from passlib.context import CryptContext

# Load environment variables from .env file
load_dotenv()

# Password hashing utility (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


async def run():
    conn_string = os.getenv("DATABASE_URL")
    if not conn_string:
        print("Connection failed. DATABASE_URL is empty or not set.")
        return

    conn = None

    try:
        conn = await asyncpg.connect(conn_string)
        print("Connection established.")

        # Drop table if it exists
        await conn.execute("DROP TABLE IF EXISTS users;")
        print("Dropped existing users table.")

        # Create users table
        await conn.execute(
            """
            CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            );
            """
        )
        print("Created users table.")

        # Insert one user with hashed password
        hashed_pwd = hash_password("mysecretpassword")

        await conn.execute(
            """
            INSERT INTO users (username, email, password)
            VALUES ($1, $2, $3);
            """,
            "unaisshaikh",  # username
            "unais@example.com",  # email
            hashed_pwd,  # hashed password
        )

        print("Inserted one sample user.")

    except Exception as e:
        print("Something went wrong:")
        print(e)
    finally:
        if conn:
            await conn.close()


# Run the async function
asyncio.run(run())
