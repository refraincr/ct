from flask import request,jsonify,Blueprint
from ct.vo import PostResponse,ApiResponse
from ct.constants import SUCCESS_CODE,EMPTY_ERROR,FORMAT_ERROR,ERROR_CODE

from ct.service import get_all_posts, upload_to_cf


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