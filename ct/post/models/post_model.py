from datetime import datetime, timezone
import sqlalchemy as sa
from sqlalchemy.orm import Mapped,mapped_column,relationship
from ct.extensions import db

from ct.models import User


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