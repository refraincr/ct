from pydantic import BaseModel
from datetime import datetime

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    username: str
    avatar: str
    create_at: datetime

    class Config:
        from_attributes = True


from typing import Optional,TypeVar,Generic
from time import time

T = TypeVar('T')

class ApiResponse(BaseModel,Generic[T]):
    code: int
    message: str = "success"
    data: Optional[T] = None
    timestamp: int = int(time())  # 秒级时间戳