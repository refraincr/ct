from flask import request,Blueprint

from ct.post.services.post_services import (get_all_posts,
                                            publish_post,
                                            get_posts_by_user_id_service)

from flask_jwt_extended import jwt_required


bp = Blueprint('post',__name__)

@bp.get('/posts')
def posts():
    return get_all_posts(request)

@bp.post('/publish')
@jwt_required()
def publish():
    return publish_post(request)

@bp.get('/posts/<int:user_id>')
@jwt_required()
def get_posts_by_user_id(user_id):
    return get_posts_by_user_id_service(request,user_id)
