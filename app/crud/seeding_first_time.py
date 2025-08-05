import asyncio
import asyncpg
import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


async def run():
    # Get the connection string from the environment variable
    conn_string = os.getenv("DATABASE_URL")
    if not conn_string:
        print("Connection failed. DATABASE_URL is empty or not set.")
    else:
        print(conn_string)
    conn = None

    try:
        conn = await asyncpg.connect(conn_string)
        print("Connection established")

        # Drop the table if it already exists
        await conn.execute("DROP TABLE IF EXISTS blog;")
        print("Finished dropping table (if it existed).")

        # Create a new table
        await conn.execute(
            """
            CREATE TABLE blogs (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                author TEXT NOT NULL,
                published BOOLEAN DEFAULT TRUE,
                tags TEXT[]
            );
        """
        )
        print("Finished creating table.")

        # Insert a single blog record (using $1, $2 for placeholders)
        await conn.execute(
            """
        INSERT INTO blogs (title, content, author, published, tags)
        VALUES ($1, $2, $3, $4, $5);
        """,
            "The Catcher in the Rye",  # title
            "A novel about teenage angst",  # content
            "J.D. Salinger",  # author
            True,  # published as boolean
            [
                "fiction",
                "classic",
                "literature",
            ],  # tags as proper list (PostgreSQL array)
        )

        print("Inserted a single blog.")

    except Exception as e:
        print("Connection failed.")
        print(e)
    finally:
        if conn:
            await conn.close()


# Run the asynchronous function
asyncio.run(run())
