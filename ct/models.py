from datetime import datetime, timezone
import sqlalchemy as sa
from sqlalchemy.orm import Mapped,mapped_column,relationship
from ct.extensions import db
from typing import Optional


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


class Post(db.Model):
    __tablename__='post'
    id: Mapped[int] = mapped_column(sa.Integer,primary_key=True)
    title: Mapped[str] = mapped_column(sa.String(20), nullable=False)
    content: Mapped[str] = mapped_column(sa.Text, nullable=False)
    create_at: Mapped[datetime] = mapped_column(sa.DateTime, default=lambda: datetime.now(timezone.utc))
    user_id: Mapped[int] = mapped_column(sa.Integer,sa.ForeignKey('users.id'),nullable=False)
    user: Mapped['User'] = relationship('User',back_populates='posts')

    def __repr__(self):
        return f'<Post {self.title} {self.content} {self.create_at}>'




