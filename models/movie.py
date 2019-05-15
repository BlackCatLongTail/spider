from models import SQLMixin, SQLBase
from sqlalchemy import Column, String


class Movie(SQLMixin, SQLBase):
    """
    存储电影信息
    """

    __tablename__ = 'Movies'

    name = Column(String(300), nullable=False, unique=True)
    score = Column(String(100), default='0')
    quote = Column(String(500), default='Nothing.')
    pic_path = Column(String(200))
    ranking = Column(String(100), default=0)

