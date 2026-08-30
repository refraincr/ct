from flask import request,Blueprint

from ct.services import (get_all_posts,
                         upload_to_cf,
                         publish_post,
                         registry_user,
                         login_user,
                         refresh_token,
                         test_token)

from flask_jwt_extended import jwt_required


bp = Blueprint('main',__name__)

@bp.get('/posts')
def posts():
    return get_all_posts()

@bp.post('/upload')
def upload():
    return upload_to_cf(request)

@bp.post('/publish')
def publish():
    return publish_post(request)

@bp.post('/registry')
def registry():
    return registry_user(request)

@bp.post('/login')
def login():
    return login_user(request)

@bp.post('/refresh')
@jwt_required(refresh=True)  # 只接受 refresh token
def refresh():
    return refresh_token()

@bp.get('/me')
@jwt_required()  # 默认只接受 access token
def me():
    return test_token()