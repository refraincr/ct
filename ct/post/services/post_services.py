from flask.wrappers import Request
from sqlalchemy import select

from ct.constants import SUCCESS_CODE, ERROR_CODE
from ct.extensions import db
from ct.post.models.post_model import Post
# 入参
from ct.post.BO.post_bo import PostPublishBO
# 响应结构
from ct.vo import PostResponse, ApiResponse


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