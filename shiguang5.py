import os
import requests
from pyquery import PyQuery as pq
import time
from models.movie import Movie


"""
爬取网页并缓存到本地
"""


def filename_form_url(url):
    # 根据url给文件取名
    f = url.split('.html')
    if len(f) == 1:
        page = 1
    else:
        page = f[0].split('-')[1]
    filename = '{}.html'.format(page)
    return filename


def save_cover(movies):
    for m in movies:
        picture_name = '{}.jpg'.format(m.ranking)
        pic_path = get_pic(m.cover_url, picture_name)  # 这里使用get只是为了将图片存储起来，并不需要返回的值
        m.pic_path = pic_path


def picture_name_form_rank(rank):
    picture_name = '{}.jpg'.format(rank)
    return picture_name


def get_pic(url, filename):
    folder = 'cached_pic'
    if not os.path.exists(folder):
        os.makedirs(folder)

    path = os.path.join(folder, filename)

    if not os.path.exists(path):
        r = requests.get(url)
        with open(path, 'wb') as f:
            f.write(r.content)

    return path


def get(url, filename):
    """
    缓存, 避免重复下载网页浪费时间
    """
    folder = 'cached_mtime'
    # 建立 cached 文件夹
    if not os.path.exists(folder):
        os.makedirs(folder)

    path = os.path.join(folder, filename)
    if os.path.exists(path):
        with open(path, 'rb') as f:
            s = f.read()
            return s
    else:
        # 发送网络请求, 把结果写入到文件夹中
        r = requests.get(url)
        with open(path, 'wb') as f:
            f.write(r.content)
            return r.content


def movie_from_div(div):
    """
    从一个 div 里面获取到一个电影信息
    """
    e = pq(div)

    # 小作用域变量用单字符
    m = Movie()
    m.name = e('.mov_con a').text()
    m.score = e('.mov_point .point').text()

    try:
        m.score = float(m.score)
    except ValueError:
        m.score = 0

    m.quote = e('.mov_con .mt3').text()
    m.cover_url = e('.mov_pic img').attr('src')
    m.ranking = e('.number em').text()
    return m


def movies_from_url(url):
    """
    从 url 中下载网页并解析出页面内所有的电影
    """
    filename = filename_form_url(url)
    page = get(url, filename)
    e = pq(page)
    items = e('.top_list li')
    # 调用 movie_from_div
    movies = [movie_from_div(i) for i in items]
    save_cover(movies)
    return movies


def main():
    start = time.time()
    url = 'http://www.mtime.com/top/movie/top100/'
    # 爬取top100首页的movie信息,因为首页url和其他url规律不同
    movies = movies_from_url(url)

    for i in range(2, 11):
        url = 'http://www.mtime.com/top/movie/top100/index-{}.html'.format(i)
        # 爬取top100首页之外的movie信息
        movies_pageleft = movies_from_url(url)
        movies += movies_pageleft

    end = time.time()
    print('duration', end - start)

    return movies


if __name__ == '__main__':
    main()
