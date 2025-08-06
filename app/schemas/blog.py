from typing import Optional, List
from pydantic import BaseModel


# === 🔹 Core Blog Schemas ===


class BlogBase(BaseModel):
    title: str
    content: str
    author: str
    published: bool = True
    tags: Optional[List[str]] = []


class BlogCreate(BlogBase):
    pass


class BlogUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None
    published: Optional[bool] = None
    tags: Optional[List[str]] = None


class BlogInDB(BlogBase):
    id: int

    class Config:
        orm_mode = True  # Optional: enables compatibility with ORM objects
