from flask import request,Blueprint

from ct.post.services.post_services import (get_all_posts,
                         publish_post)

from flask_jwt_extended import jwt_required


bp = Blueprint('post',__name__)

@bp.get('/posts')
def posts():
    return get_all_posts()

@bp.post('/publish')
def publish():
    return publish_post(request)