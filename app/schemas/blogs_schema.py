from pydantic import BaseModel
from typing import Optional, List


# Pydantic schema
class BlogCreate(BaseModel):
    title: str
    content: str
    author: str
    published: bool = True
    tags: Optional[List[str]] = None


class BlogUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None
    published: Optional[bool] = None
    tags: Optional[List[str]] = None
