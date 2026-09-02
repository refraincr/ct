from sqlalchemy.orm import DeclarativeBase
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import boto3
from botocore.config import Config
import os
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from ct.vo import ApiResponse
from ct.constants import TOKEN_MISSING,TOKEN_EXPIRED,TOKEN_INVALID


load_dotenv()

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

migrate = Migrate()

r2_client = boto3.client(
    service_name='s3',
    endpoint_url=f"https://{os.getenv('CF_ACCOUNT_ID')}.r2.cloudflarestorage.com",
    aws_access_key_id=os.getenv('CF_R2_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('CF_R2_SECRET_KEY'),
    config=Config(signature_version='s3v4'),
    region_name='auto'
)

BUCKET_NAME = os.getenv('CF_R2_BUCKET_NAME')
PUBLIC_DOMAIN = os.getenv('CF_R2_PUBLIC_DOMAIN')

jwt = JWTManager()

@jwt.user_identity_loader
def user_identity_loader(user):
    """根据这个来生成token"""
    return str(user.id)

@jwt.user_lookup_loader
def user_lookup_loader(_jwt_header,jwt_data):
    """校验 token 后查出 User 对象赋值给 current_user"""
    from ct.user.models.user_model import User
    # 延时导入，防止循环导入
    user_id = int(jwt_data['sub'])
    return User.get_user_by_id(user_id)

# 统一错误处理
@jwt.unauthorized_loader
def unauthorized_loader(error_string):
    return ApiResponse(code=TOKEN_MISSING,message='未提供登录凭证').model_dump(),401

@jwt.expired_token_loader
def expired_token_loader(jwt_header, jwt_data):
    return ApiResponse(code=TOKEN_EXPIRED,message='登录凭证已过期').model_dump(),401

@jwt.invalid_token_loader
def invalid_token_loader(error_string):
    return ApiResponse(code=TOKEN_INVALID,message='无效的登录凭证').model_dump(),401


if __name__ == '__main__':
    print(os.getenv('CF_ACCOUNT_ID'))