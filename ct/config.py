class Config:
    # 防止用户恶意修改 cookies
    SECRET_KEY = '948abfc4bff796dc469534692bcbde09'
    # 数据库连接 uri
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/ct'
    # 不需要额外监控对象的变化
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    HOST = 'localhost'

    PORT = 5001


class Development(Config):
    DEBUG = True

config_map = {
    'development': Development
}