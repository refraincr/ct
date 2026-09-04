from flask import request,Blueprint

from ct.user.services.user_services import (registry_user,
                                            login_user,
                                            refresh_token,
                                            test_token,
                                            upload_to_cf,
                                            user_info_service)

from flask_jwt_extended import jwt_required


bp = Blueprint('user',__name__)

@bp.post('/upload')
def upload():
    return upload_to_cf(request)

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

@bp.get('/user/info')
@jwt_required()
def user_info():
    return user_info_service(request)