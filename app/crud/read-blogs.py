import asyncio
import os

import asyncpg
from dotenv import load_dotenv

load_dotenv()


async def run():
    conn_string = os.getenv("DATABASE_URL")
    conn = None

    try:
        conn = await asyncpg.connect(conn_string)
        print("Connection established")

        # Fetch all rows from the books table
        rows = await conn.fetch("SELECT * FROM blogs ORDER BY id;")

        print("\n--- Blogs ---")
        for row in rows:
            # asyncpg rows can be accessed by index or column name
            print(f"ID: {row['id']}")
            print(f"Title: {row['title']}")
            print(f"Content: {row['content']}")
            print(f"Author: {row['author']}")
            print(f"Published: {row['published']}")
            print("Tags:")
            if row["tags"]:
                for tag in row["tags"]:
                    print(f" - {tag}")
            else:
                print(" - None")

        print("--------------------\n")

    except Exception as e:
        print("Connection failed.")
        print(e)
    finally:
        if conn:
            await conn.close()


asyncio.run(run())
