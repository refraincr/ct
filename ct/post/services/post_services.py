from ct.models import User, Post
from sqlalchemy import select
from flask.wrappers import Request
import uuid
from ct.extensions import r2_client, BUCKET_NAME, PUBLIC_DOMAIN, db
from ct.constants import SUCCESS_CODE, EMPTY_ERROR, FORMAT_ERROR, ERROR_CODE
import io

# 响应结构
from ct.vo import PostResponse, ApiResponse

# 入参
from ct.bo import PostPublishBO, RegistryFormBO, LoginBO

from flask_jwt_extended import get_jwt_identity, create_access_token, create_refresh_token


def get_all_posts() -> tuple[ApiResponse, int]:
    result: list[PostResponse] = []
    stmt = select(Post)
    data: list[Post] = db.session.execute(stmt).scalars().all()
    for i in range(len(data)):
        user = data[i].user
        result.append(PostResponse(
            title=data[i].title,
            content=data[i].content,
            create_at=data[i].create_at,
            username=user.username,
            avatar=user.avatar
        ))

    return ApiResponse(code=SUCCESS_CODE, data=result).model_dump(), 200

def publish_post(req: Request) -> tuple[ApiResponse, int]:
    # 入参验证
    try:
        postPublish = PostPublishBO(**req.get_json())
    except ValueError as e:
        resp = ApiResponse(
            code=ERROR_CODE,
            message=str(e)
        )
        return resp.model_dump(), 443

    p = Post(**postPublish.model_dump())

    try:
        with db.session.begin():
            db.session.add(p)
    except Exception as e:
        print(f'保存失败: {str(e)}')

    resp = ApiResponse(
        code=SUCCESS_CODE,
        data=None
    )
    return resp.model_dump(), 200