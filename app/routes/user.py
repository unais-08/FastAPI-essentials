from fastapi import APIRouter, Request, status, HTTPException, Path
from app.schemas.user import UserBase, UserOut, UserUpdate
from app.schemas.response import APIResponse, APIListResponse
from app.utils.security import hash_password

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=APIListResponse[UserOut])
async def get_users(request: Request):
    db_pool = request.app.state.db_pool
    query = "SELECT id, username, email FROM users"

    async with db_pool.acquire() as conn:
        rows = await conn.fetch(query)
        users = [dict(row) for row in rows]

    return {
        "success": True,
        "message": "Users retrieved successfully",
        "data": users,
    }


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=APIResponse[UserOut]
)
async def create_user(request: Request, user: UserBase):
    db_pool = request.app.state.db_pool
    hashed_pwd = hash_password(user.password)

    query = """
    INSERT INTO users (username, email, password)
    VALUES ($1, $2, $3)
    RETURNING id, username, email;
    """

    async with db_pool.acquire() as conn:
        row = await conn.fetchrow(query, user.username, user.email, hashed_pwd)

    return {
        "success": True,
        "message": "User created successfully",
        "data": dict(row),
    }


@router.put("/{user_id}", response_model=APIResponse[UserOut])
async def update_user(
    request: Request, user_id: int = Path(..., gt=0), user: UserUpdate = ...
):
    db_pool = request.app.state.db_pool
    fields = []
    values = []

    if user.username:
        fields.append("username = $" + str(len(values) + 1))
        values.append(user.username)

    if user.email:
        fields.append("email = $" + str(len(values) + 1))
        values.append(user.email)

    if user.password:
        fields.append("password = $" + str(len(values) + 1))
        values.append(hash_password(user.password))

    if not fields:
        raise HTTPException(status_code=400, detail="No fields to update.")

    query = f"""
        UPDATE users SET {", ".join(fields)}
        WHERE id = ${len(values) + 1}
        RETURNING id, username, email;
    """
    values.append(user_id)

    async with db_pool.acquire() as conn:
        row = await conn.fetchrow(query, *values)
        if not row:
            raise HTTPException(status_code=404, detail="User not found")

    return {
        "success": True,
        "message": "User updated successfully",
        "data": dict(row),
    }


@router.delete("/{user_id}", response_model=APIResponse[None])
async def delete_user(request: Request, user_id: int = Path(..., gt=0)):
    db_pool = request.app.state.db_pool

    query = "DELETE FROM users WHERE id = $1 RETURNING id;"
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow(query, user_id)

        if not row:
            raise HTTPException(status_code=404, detail="User not found")

    return {
        "success": True,
        "message": "User deleted successfully",
        "data": None,
    }
