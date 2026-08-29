from flask import request,jsonify,Blueprint
from ct.vo import PostResponse,ApiResponse
from ct.constants import SUCCESS_CODE

from ct.services import (get_all_posts,
                         upload_to_cf,
                         publish_post,
                         registry_user,
                         login_user)


bp = Blueprint('main',__name__)

@bp.get('/posts')
def posts():
    api_resp = ApiResponse[list[PostResponse]](
        code=SUCCESS_CODE,
        data=get_all_posts()
    )
    return jsonify(api_resp.model_dump()), 200


@bp.post('/upload')
def upload():
    resp,status_code = upload_to_cf(request)
    return jsonify(resp.model_dump()),status_code

@bp.post('/publish')
def publish():
    resp,status_code = publish_post(request)
    return jsonify(resp.model_dump()),status_code

@bp.post('/registry')
def registry():
    resp,status_code = registry_user(request)
    return jsonify(resp.model_dump()),status_code

@bp.post('/login')
def login():
    resp,status_code = login_user(request)
    return jsonify(resp.model_dump()),status_code