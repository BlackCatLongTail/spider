from models import SQLMixin, SQLBase
from sqlalchemy import Column, String, Float


class Movie(SQLMixin, SQLBase):
    """
    存储电影信息
    """

    __tablename__ = 'Movies'

    name = Column(String(300), nullable=False, unique=True)
    score = Column(Float(53), default=0)
    quote = Column(String(500), default='Nothing.')
    pic_path = Column(String(200))
    ranking = Column(String(100), default=0)

    @classmethod
    def find_one(cls, sql_expression):
        m = super().find_one(sql_expression)
        return m

    @classmethod
    def find_all(cls, sql_expression):
        ms = super().find_all(sql_expression)
        return ms






