from ct.extensions import db,migrate,jwt
from dotenv import load_dotenv
import os
from flask import Flask
from ct.config import config_map
from flask_cors import CORS

load_dotenv()

def create_app(config_name: str | None = None)->Flask:
    config_name = config_name or os.getenv('config_name','development')

    app = Flask(__name__)
    CORS(app)

    # 加载配置
    app.config.from_object(config_map[config_name])

    jwt.init_app(app)
    db.init_app(app)
    migrate.init_app(app,db)


    # 导入模型，确保它们被注册到 db.Model 的 metadata 里
    # Flask-Migrate生成迁移脚本时才能检测到这些
    from ct.user.models.user_model import User
    from ct.post.models.post_model import Post

    # 导入蓝图
    from ct.user.routes.user_routes import bp as user_bp
    from ct.post.routes.post_routes import bp as post_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(post_bp)

    return app


if __name__ == '__main__':
    flask_app = create_app('development')
    flask_app.run(
        flask_app.config['HOST'],
        flask_app.config['PORT'],
        flask_app.config['DEBUG'],
        use_reloader = flask_app.config['USE_RELOADER'],
    )