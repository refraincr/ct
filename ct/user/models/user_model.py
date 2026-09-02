import sqlalchemy as sa
from sqlalchemy.orm import Mapped,mapped_column,relationship
from ct.extensions import db
import bcrypt
from ct.post.models.post_model import Post

class User(db.Model):
    __tablename__='users'
    id: Mapped[int] = mapped_column(sa.Integer,primary_key=True)
    username: Mapped[str] = mapped_column(sa.String(20),unique=True, nullable=False)
    email: Mapped[str] = mapped_column(sa.String(120),unique=True, nullable=False)
    password: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    avatar: Mapped[str] = mapped_column(sa.String(255),nullable=True,default='default.jpg')
    posts: Mapped[list['Post']] = relationship('Post', back_populates='user', lazy='select')

    def __repr__(self):
        return f'<User id={self.id} username={self.username} email={self.email}>'

    @classmethod
    def get_user_by_username(cls,username: str) -> 'User | None':
        stmt = db.select(cls).where(cls.username == username)
        return db.session.execute(stmt).scalar_one_or_none()

    @classmethod
    def get_user_by_email(cls,email: str) -> 'User | None':
        stmt = db.select(cls).where(cls.email == email)
        return db.session.execute(stmt).scalar_one_or_none()

    @classmethod
    def get_user_by_id(cls,user_id: int) -> 'User | None':
        return db.session.get(User,user_id)

    @classmethod
    def generate_password_hash(cls,password: str) -> str:
        password_byte = password.encode('utf-8')
        salt = bcrypt.gensalt()
        password_byte_hash = bcrypt.hashpw(password_byte, salt)
        return password_byte_hash.decode('utf-8')

    @classmethod
    def check_password(cls, password: str, saved_password: str) -> bool:
        """ 前面的输入的密码，后面的是保存的密码 """
        return bcrypt.checkpw(password.encode('utf-8'), saved_password.encode('utf-8'))
