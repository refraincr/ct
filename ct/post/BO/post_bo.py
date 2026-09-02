from pydantic import BaseModel,Field

class PostPublishBO(BaseModel):
    title: str = Field(min_length=1,max_length=20)
    content: str = Field(min_length=1)
    user_id: int = Field(gt=0)