from sqlalchemy.orm import DeclarativeBase
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import boto3
from botocore.config import Config
import os
from dotenv import load_dotenv


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

if __name__ == '__main__':
    print(os.getenv('CF_ACCOUNT_ID'))