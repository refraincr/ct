from pydantic import BaseModel
from datetime import datetime

class PostResponse(BaseModel):
    title: str
    content: str
    user_id: int
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