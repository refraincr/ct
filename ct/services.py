from ct.models import User,Post
from datetime import datetime
from flask.wrappers import Request
import uuid
from ct.extensions import r2_client,BUCKET_NAME,PUBLIC_DOMAIN,db
from ct.constants import SUCCESS_CODE,EMPTY_ERROR,FORMAT_ERROR,ERROR_CODE

# 响应结构
from ct.vo import PostResponse,ApiResponse

# 入参
from ct.bo import PostPublishBO,RegistryFormBO,LoginBO

from flask_jwt_extended import get_jwt_identity,create_access_token,create_refresh_token

posts_data = [
    {
        'title': '清灰换硅脂真有用',
        'content':'以玩三角洲为例：清灰换硅脂前温度最高92摄氏度帧率最高100帧，清灰换硅脂后温度最高67摄氏度帧率最高200帧',
        'user_id': 1,
        'create_at': datetime.now()
    },
    {
        'title': '升级硬件啦',
        'content': '加装了 8G 4800mt/s 的内存条和512G的2.5寸固态硬盘（实际上只有480g左右）,终于可以下得了三角洲了...',
        'user_id': 1,
        'create_at': datetime.now()
    }
]

def get_all_posts()->tuple[ApiResponse,int]:
    mock_data = []
    for i in range(0,len(posts_data)):
        mock_data.append(PostResponse(
            title=posts_data[i]['title'],
            content=posts_data[i]['content'],
            user_id=posts_data[i]['user_id'],
            create_at=posts_data[i]['create_at']
        ))
    return ApiResponse(code=SUCCESS_CODE,data=mock_data).model_dump(),200

def upload_to_cf(req: Request) -> tuple[ApiResponse,int]:
    """ (上传返回的路径信息, message, 状态码) """
    if 'avatar' not in req.files:
        resp = ApiResponse(
            code=FORMAT_ERROR,
            data=None,
            message='未提供文件'
        )
        return resp.model_dump(), 200
    
    file = req.files['avatar']
    if file.filename == '':
        resp = ApiResponse(
            code=EMPTY_ERROR,
            data=None,
            message='未选择文件'
        )
        return resp.model_dump(), 200

    ext = file.filename.rsplit('.',1)[-1] if '.' in file.filename else 'png'
    filename = f'images/{uuid.uuid4().hex}.{ext}'

    try:
        r2_client.upload_fileobj(
            file,
            BUCKET_NAME,
            filename,
            ExtraArgs={
                'ContentType': file.content_type or 'image/jpeg'
            }
        )
        image_url = f'{PUBLIC_DOMAIN}/{filename}'

        resp = ApiResponse[dict[str,str]](
            code=SUCCESS_CODE,
            data={
                'filename': filename,
                'url': image_url
            },
            message='上传成功'
        )
        return resp.model_dump(),200

    except Exception as e:
        resp = ApiResponse(
            code=ERROR_CODE,
            data=None,
            message=str(e)
        )
        return resp.model_dump(),500

def publish_post(req: Request) -> tuple[ApiResponse,int]:
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
    return resp.model_dump(),200

def registry_user(req: Request) -> tuple[ApiResponse,int]:
    # 验证参数
    try:
        registry_form = RegistryFormBO(**req.get_json())
    except ValueError as e:
        resp = ApiResponse(
            code=ERROR_CODE,
            message=str(e)
        )
        return resp.model_dump(),443

    u = User(
        username = registry_form.username,
        email = registry_form.email,
        password = User.generate_password_hash(registry_form.password),
        avatar = registry_form.avatar
    )

    try:
        with db.session.begin():
            db.session.add(u)
    except Exception as e:
        resp = ApiResponse(
            code=ERROR_CODE,
            message='用户保存失败'
        )
        return resp.model_dump(), 200

    resp = ApiResponse(
        code=SUCCESS_CODE,
        message='用户创建成功'
    )
    return resp.model_dump(),200

def login_user(req: Request) -> tuple[ApiResponse,int]:
    try:
        login_bo = LoginBO(**req.get_json())
    except ValueError as e:
        resp = ApiResponse(
            code=ERROR_CODE,
            message=str(e)
        )

        return resp.model_dump(),443

    if User.get_user_by_username(login_bo.username):
        user = User.get_user_by_username(login_bo.username)
        is_valid = User.check_password(login_bo.password,user.password)

        if is_valid:
            _refresh_token = create_refresh_token(user)
            _access_token = create_access_token(user)
            return ApiResponse(code=SUCCESS_CODE,
                               message='登录成功',
                               data={
                                   'refresh_token': _refresh_token,
                                   'access_token': _access_token
                               }).model_dump(), 200
        else:

            return ApiResponse(code=ERROR_CODE,message='登录失败,用户名（邮箱）或密码错误').model_dump(), 200

    resp = ApiResponse(
        code=EMPTY_ERROR,
        message='用户信息不存在'
    )

    return resp.model_dump(), 200

def refresh_token() -> tuple[ApiResponse,int]:
    user_id = int(get_jwt_identity())
    from ct.models import User
    user = User.get_user_by_id(user_id)
    access_token = create_access_token(user)

    return ApiResponse(code=SUCCESS_CODE,data={'access_token':access_token}).model_dump(),200

def test_token() -> tuple[ApiResponse,int]:
    return ApiResponse(code=SUCCESS_CODE).model_dump(),200