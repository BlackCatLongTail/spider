from shiguang5 import main as spider
from models.movie import Movie


def main():
    ms = spider()
    if len(ms) == 100:
        Movie.save_all(ms)
        print('成功爬取所有页面并存入数据库')
    else:
        print('爬取页面有遗漏')


if __name__ == '__main__':
    main()

