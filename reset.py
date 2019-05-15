from models import reset_database
from models.movie import Movie

if __name__ == '__main__':
    # Movie没被显式调用也要导入，因为在操作室中需要查找类来创建表
    reset_database()
