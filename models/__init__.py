import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import config


def reset_database():
    url = 'mysql+pymysql://root:{}@127.0.0.1:3306/?charset=utf8mb4'.format(
        config.mysql_password
    )
    print('sql url', url)
    e = sqlalchemy.create_engine(url, echo=True)

    with e.connect() as c:
        c.execute('DROP DATABASE IF EXISTS mtime')
        c.execute('CREATE DATABASE mtime CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
        c.execute('USE mtime')

    SQLBase.metadata.create_all(bind=e)


SQLBase = declarative_base()


def configured_engine():
    url = 'mysql+pymysql://root:{}@127.0.0.1:3306/mtime?charset=utf8mb4'.format(
        config.mysql_password
    )
    #  长时间不操作的情况下MySQL会关闭连接，所以进行定时唤醒
    e = sqlalchemy.create_engine(url, echo=True, pool_recycle=3600)
    return e


class SQLMixin(object):
    """
    基类, 用来显示类的信息
    """
    session = scoped_session(sessionmaker(bind=configured_engine()))
    query = session.query_property()

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    deleted = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=False)

    @classmethod
    def new(cls, **kwargs):
        m = cls()
        # User.id = id
        for name, value in kwargs.items():
            setattr(m, name, value)

        SQLMixin.session.add(m)
        SQLMixin.session.commit()

        return m

    @classmethod
    def delete(cls, id):
        # 实现的是假删除，实际上在数据库中并没有删除这一行
        cls.update(id, deleted=True)

    @classmethod
    def update(cls, id, **kwargs):
        m = cls.query.filter_by(id=id).first()
        for name, value in kwargs.items():
            setattr(m, name, value)

        SQLMixin.session.add(m)
        SQLMixin.session.commit()

        return m

    @classmethod
    def all(cls, **kwargs):
        # 只显示所有deleted字段为False的对象
        kwargs['deleted'] = False
        ms = cls.query.filter_by(**kwargs).all()
        return ms

    @classmethod
    def find_all(cls, sql_expression):
        ms = cls.query.filter(sql_expression, cls.deleted == False).all()
        return ms

    @classmethod
    def one(cls, **kwargs):
        kwargs['deleted'] = False
        m = cls.query.filter_by(**kwargs).first()
        return m

    @classmethod
    def find_one(cls, sql_expression):
        # kwargs['deleted'] = False
        m = cls.query.filter(sql_expression, cls.deleted == False).first()
        return m

    @classmethod
    def exist(cls, **kwargs):
        # windows 下 literal(True) 有 bug
        kwargs['deleted'] = False
        e = sqlalchemy.exists()
        for name, value in kwargs.items():
            e = e.where(getattr(cls, name) == value)

        r = cls.session.query(e).scalar()

        return r

    def save(self):
        SQLMixin.session.add(self)
        SQLMixin.session.commit()

    @staticmethod
    def save_all(ms):
        SQLMixin.session.add_all(ms)
        SQLMixin.session.commit()

    def __repr__(self):
        name = self.__class__.__name__
        properties = ('{}=({})'.format(k, v) for k, v in self.__dict__.items())
        s = '\n<{} \n  {}>'.format(name, '\n  '.join(properties))
        return s