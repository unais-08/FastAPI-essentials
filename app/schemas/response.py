from typing import Generic, Optional, List, TypeVar
from pydantic.generics import GenericModel

T = TypeVar("T")


class APIResponse(GenericModel, Generic[T]):
    success: bool
    message: str
    data: Optional[T] = None


class APIListResponse(GenericModel, Generic[T]):
    success: bool
    message: str
    data: Optional[List[T]] = None
