"""
业务对象(入参)
"""

from pydantic import BaseModel,Field,EmailStr,field_validator
from typing import Optional

class PostPublishBO(BaseModel):
    title: str = Field(min_length=1,max_length=20)
    content: str = Field(min_length=1)
    user_id: int = Field(gt=0)

class RegistryFormBO(BaseModel):
    username: str = Field(min_length=1,max_length=20)
    email: EmailStr
    password: str = Field(min_length=8,max_length=128)
    avatar: Optional[str] = Field(min_length=8,max_length=255,default=None)

    @field_validator('password')
    @classmethod
    def validate_password(cls,v: str)->str:
        # any 存在
        if not any(c.isdigit() for c in v):
            raise ValueError('至少包含一个数字')
        if not any(c.isalpha() for c in v):
            raise ValueError('至少包含一个字母')
        return v


class LoginBO(BaseModel):
    username: str = Field(min_length=1,max_length=20)
    password: str = Field(min_length=8,max_length=128)
