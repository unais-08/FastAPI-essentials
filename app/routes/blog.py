from fastapi import APIRouter, Request, HTTPException
from typing import Optional, Literal
from app.schemas.blogs_schema import BlogCreate, BlogUpdate

router = APIRouter()


@router.get("/blogs")
async def retrieve_blogs(
    request: Request,
    published: Optional[bool] = None,
    limit: Optional[int] = None,
    sort: Literal["asc", "desc"] = "asc",
):
    db_pool = request.app.state.db_pool
    query = "SELECT * FROM blogs"

    async with db_pool.acquire() as conn:
        rows = await conn.fetch(query)

    return [dict(row) for row in rows]


@router.post("/blogs")
async def create_blog(request: Request, blog: BlogCreate):
    db_pool = request.app.state.db_pool

    query = """
    INSERT INTO blogs (title, content, author, published, tags)
    VALUES ($1, $2, $3, $4, $5)
    RETURNING id, title, content, author, published, tags;
    """

    async with db_pool.acquire() as conn:
        row = await conn.fetchrow(
            query, blog.title, blog.content, blog.author, blog.published, blog.tags
        )

    return dict(row)


@router.put("/blogs/{blog_id}")
async def edit_blog(request: Request, blog_id: int, blog: BlogUpdate):
    db_pool = request.app.state.db_pool

    # Fetch existing blog
    async with db_pool.acquire() as conn:
        existing = await conn.fetchrow("SELECT * FROM blogs WHERE id = $1", blog_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Blog not found")

        # Prepare updated fields, fallback to existing if not provided
        updated_title = blog.title if blog.title is not None else existing["title"]
        updated_content = (
            blog.content if blog.content is not None else existing["content"]
        )
        updated_author = blog.author if blog.author is not None else existing["author"]
        updated_published = (
            blog.published if blog.published is not None else existing["published"]
        )
        updated_tags = blog.tags if blog.tags is not None else existing["tags"]

        query = """
        UPDATE blogs
        SET title = $1, content = $2, author = $3, published = $4, tags = $5
        WHERE id = $6
        RETURNING id, title, content, author, published, tags;
        """

        row = await conn.fetchrow(
            query,
            updated_title,
            updated_content,
            updated_author,
            updated_published,
            updated_tags,
            blog_id,
        )

    return dict(row)


@router.delete("/blogs/{blog_id}")
async def delete_blog(request: Request, blog_id: int):
    db_pool = request.app.state.db_pool

    query = "DELETE FROM blogs WHERE id = $1 RETURNING id;"

    async with db_pool.acquire() as conn:
        row = await conn.fetchrow(query, blog_id)
        if not row:
            raise HTTPException(status_code=404, detail="Blog not found")

    return {"message": "Blog deleted", "id": row["id"]}
