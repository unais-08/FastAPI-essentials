from fastapi import APIRouter, Request, HTTPException, status


from app.schemas.blog import BlogCreate, BlogUpdate, BlogBase, BlogInDB
from app.schemas.response import APIResponse, APIListResponse

router = APIRouter(prefix="/blogs", tags=["Blogs"])


@router.get("/", response_model=APIListResponse[BlogInDB])
async def get_blogs(request: Request):
    db_pool = request.app.state.db_pool
    query = "SELECT * FROM blogs"

    async with db_pool.acquire() as conn:
        rows = await conn.fetch(query)
        blogs = [dict(row) for row in rows]

    return {
        "success": True,
        "message": "Blogs retrieved successfully",
        "data": blogs,
    }


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=APIResponse[BlogInDB]
)
async def create_blog(request: Request, blog: BlogCreate):
    db_pool = request.app.state.db_pool

    query = """
    INSERT INTO blogs (title, content, author, published, tags)
    VALUES ($1, $2, $3, $4, $5)
    RETURNING id, title, content, author, published, tags;
    """

    async with db_pool.acquire() as conn:
        row = await conn.fetchrow(
            query,
            blog.title,
            blog.content,
            blog.author,
            blog.published,
            blog.tags,
        )

    return {
        "success": True,
        "message": "Blog created successfully",
        "data": dict(row),
    }


@router.put("/{blog_id}", response_model=APIResponse[BlogInDB])
async def update_blog(request: Request, blog_id: int, blog: BlogUpdate):
    db_pool = request.app.state.db_pool

    async with db_pool.acquire() as conn:
        # Check if blog exists
        existing = await conn.fetchrow("SELECT * FROM blogs WHERE id = $1", blog_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Blog not found")

        # Merge updates
        updated_title = blog.title or existing["title"]
        updated_content = blog.content or existing["content"]
        updated_author = blog.author or existing["author"]
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

    return {
        "success": True,
        "message": "Blog updated successfully",
        "data": dict(row),
    }


@router.delete("/{blog_id}", response_model=APIResponse[dict])
async def delete_blog(request: Request, blog_id: int):
    db_pool = request.app.state.db_pool

    query = "DELETE FROM blogs WHERE id = $1 RETURNING id;"

    async with db_pool.acquire() as conn:
        row = await conn.fetchrow(query, blog_id)

        if not row:
            raise HTTPException(status_code=404, detail="Blog not found")

    return {
        "success": True,
        "message": "Blog deleted successfully",
        "data": {"id": row["id"]},
    }
