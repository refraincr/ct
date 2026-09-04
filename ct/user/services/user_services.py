import io
import uuid

from flask.wrappers import Request
from flask_jwt_extended import get_jwt_identity, create_access_token, create_refresh_token

# 入参
from ct.user.BO.user_bo import RegistryFormBO, LoginBO
from ct.constants import SUCCESS_CODE, EMPTY_ERROR, FORMAT_ERROR, ERROR_CODE
from ct.extensions import r2_client, BUCKET_NAME, PUBLIC_DOMAIN, db
from ct.user.models.user_model import User
# 响应结构
from ct.vo import ApiResponse


def upload_to_cf(req: Request) -> tuple[ApiResponse, int]:
    """ (上传返回的路径信息, message, 状态码) """
    if 'avatar' not in req.files:
        resp = ApiResponse(
            code=FORMAT_ERROR,
            data=None,
            message='未提供文件'
        )
        return resp.model_dump(), 400

    file = req.files['avatar']
    if file.filename == '':
        resp = ApiResponse(
            code=EMPTY_ERROR,
            data=None,
            message='未选择文件'
        )
        return resp.model_dump(), 400

    ext = file.filename.rsplit('.', 1)[-1] if '.' in file.filename else 'png'
    filename = f'images/{uuid.uuid4().hex}.{ext}'

    try:
        raw_bytes = file.read()
        content_type = file.content_type or 'image/jpeg'
        r2_client.upload_fileobj(
            io.BytesIO(raw_bytes),
            BUCKET_NAME,
            filename,
            ExtraArgs={
                'ContentType': content_type or 'image/jpeg'
            }
        )
        from ct.utils import image_process_and_upload
        thumbnail_url = image_process_and_upload(raw_bytes, content_type, filename)
        image_url = f'{PUBLIC_DOMAIN}/{filename}'

        resp = ApiResponse[dict[str, str]](
            code=SUCCESS_CODE,
            data={
                'thumbnail_url': thumbnail_url,
                'filename': filename,
                'url': image_url
            },
            message='上传成功'
        )
        return resp.model_dump(), 200

    except Exception as e:
        resp = ApiResponse(
            code=ERROR_CODE,
            data=None,
            message=str(e)
        )
        return resp.model_dump(), 500

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
    from ct.user.models.user_model import User
    user = User.get_user_by_id(user_id)
    access_token = create_access_token(user)

    return ApiResponse(code=SUCCESS_CODE,data={'access_token':access_token}).model_dump(),200

def test_token() -> tuple[ApiResponse,int]:
    return ApiResponse(code=SUCCESS_CODE).model_dump(),200

def user_info_service() -> tuple[ApiResponse,int]:
    user_id = int(get_jwt_identity())
    from ct.user.models.user_model import User
    user = User.get_user_by_id(user_id)
    user_info = {
        'username': user.username,
        'id': user.id,
        'avatar': user.avatar,
        'email': user.email
    }
    return ApiResponse(code=SUCCESS_CODE,data=user_info).model_dump(),200