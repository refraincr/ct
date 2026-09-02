from flask.wrappers import Request
from sqlalchemy import select,func


from ct.constants import SUCCESS_CODE, ERROR_CODE
from ct.extensions import db
from ct.post.models.post_model import Post
from ct.user.models.user_model import User
# 入参
from ct.post.BO.post_bo import PostPublishBO
# 响应结构
from ct.vo import PostResponse, ApiResponse


def get_all_posts(request: Request) -> tuple[ApiResponse, int]:
    try:
        page = max(int(request.args.get('page',1)),1)
        page_size = min(max(int(request.args.get('page_size',10)),1),100)
    except ValueError:
        return ApiResponse(code=ERROR_CODE,message='分页参数错误').model_dump(),400

    # 获取数据总量
    total_stmt = select(func.count()).select_from(Post)
    total: int = db.session.execute(total_stmt).scalar_one()

    # 获取分页数据
    stmt = (
        select(Post)
        .order_by(Post.create_at.desc())
        .offset((page-1)*page_size)
        .limit(page_size)
    )
    data = db.session.execute(stmt).scalars().all()

    select_result = [
        PostResponse(
            title=post.title,
            content=post.content,
            username=post.user.username,
            avatar=post.user.avatar,
            create_at=post.create_at
        )
        for post in data
    ]

    result = {
        'result': select_result,
        'total': total,
        'page': page,
        'page_size': page_size,
        'total_pages': (total + page_size - 1) // page_size
    }

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
        db.session.add(p)
    except Exception as e:
        return ApiResponse(code=ERROR_CODE,message=str(e)).model_dump(), 500

    resp = ApiResponse(
        code=SUCCESS_CODE,
        data=None
    )
    return resp.model_dump(), 200

def get_posts_by_user_id_service(request: Request,user_id: int) -> tuple[ApiResponse, int]:
    try:
        page = max(int(request.args.get('page',1)),1)
        page_size = min(max(int(request.args.get('page_size',10)),1),100)
    except ValueError:
        return ApiResponse(code=ERROR_CODE,message='参数错误').model_dump(),400

    user = db.session.get(User,user_id)
    total = len(user.posts)
    stmt = (
        select(Post)
        .where(Post.user_id == user_id)
        .order_by(Post.create_at.desc())
        .offset((page-1)*page_size)
        .limit(page_size)
    )
    data = db.session.execute(stmt).scalars().all()

    select_result = [
        PostResponse(
            title=post.title,
            content=post.content,
            username=post.user.username,
            avatar=post.user.avatar,
            create_at=post.create_at
        )
        for post in data
    ]

    result = {
        'result':select_result,
        'total': total,
        'page': page,
        'page_size': page_size,
        'total_pages': (total + page_size - 1) // page_size
    }
    return ApiResponse(code=SUCCESS_CODE,data=result).model_dump(),200
