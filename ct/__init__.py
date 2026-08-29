# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_cors import CORS
# import boto3
# from botocore.config import Config
# from dotenv import load_dotenv
#
# load_dotenv()
# import os
#
# app = Flask(__name__)
# CORS(app)
# app.config['SECRET_KEY'] = '948abfc4bff796dc469534692bcbde09'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/ct'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 不需要额外监控对象的变化
# db = SQLAlchemy(app)
#
#
# # 示例化 cf 客户端
# r2_client = boto3.client(
#     service_name='s3',
#     endpoint_url=f"https://{os.getenv('CF_ACCOUNT_ID')}.r2.cloudflarestorage.com",
#     aws_access_key_id=os.getenv('CF_R2_ACCESS_KEY'),
#     aws_secret_access_key=os.getenv('CF_R2_SECRET_KEY'),
#     config=Config(signature_version='s3v4'),
#     region_name='auto'
# )
#
# BUCKET_NAME = os.getenv('CF_R2_BUCKET_NAME')
# PUBLIC_DOMAIN = os.getenv('CF_R2_PUBLIC_DOMAIN')
#
# from ct import routes