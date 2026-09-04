from flask.wrappers import Request
from sqlalchemy import select, func, or_

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
            id=post.id,
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
        db.session.commit()
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

    content = request.args.get('content','')
    start = request.args.get('start','')
    end = request.args.get('end','')

    user = db.session.get(User,user_id)
    total = len(user.posts)
    condition = [Post.user_id == user_id]
    if content:
        condition.append(or_(Post.title.like(f'%{content}%'),Post.content.like(f'%{content}%')))
    from datetime import datetime
    if start:
        start_time = datetime.strptime(start,'%Y-%m-%d')
        condition.append(start_time <= Post.create_at)

    if end:
        end_time = datetime.strptime(end,'%Y-%m-%d')
        condition.append(end_time >= Post.create_at)

    stmt = (
        select(Post)
        .where(*condition)
        .order_by(Post.create_at.desc())
        .offset((page-1)*page_size)
        .limit(page_size)
    )
    data = db.session.execute(stmt).scalars().all()

    select_result = [
        PostResponse(
            id=post.id,
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

def del_post_by_id_service(post_id: int) -> tuple[ApiResponse, int]:
    post = db.session.get(Post, post_id)
    if not post:
        return ApiResponse(code=ERROR_CODE,message='没有该数据').model_dump(),400

    db.session.delete(post)
    db.session.commit()

    return ApiResponse(code=SUCCESS_CODE,message='删除成功').model_dump(),200

def update_post_by_id_service(request:Request,post_id: int) -> tuple[ApiResponse, int]:
    post = db.session.get(Post,post_id)
    if not post:
        return ApiResponse(code=ERROR_CODE,message='没有该数据').model_dump(),400

    post.title = request.get_json()['title'] or post.title
    post.content =  request.get_json()['content'] or post.content

    db.session.commit()

    return ApiResponse(code=SUCCESS_CODE, message='更新成功').model_dump(), 200