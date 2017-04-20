import os.path
import time
import json


def log(*args, **kwargs):
    # time.time() 返回 unix time
    # 如何把 unix time 转换为普通人类可以看懂的格式呢？
    format = '%H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    with open('log.gua.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)


def datetimeformat(value, format="%B %d %Y"):
    value = time.localtime(value)
    dt = time.strftime(format, value)
    return dt



def abstract(value, length=150):
    lv = len(value)
    if lv > 150:
        abs = value[:length] + '... ...'
    else:
        abs = value
    return abs


def partiton(li, a, b):
    key = li[a]
    while a < b:
        while a < b and li[b] <= key:
            b -= 1
        while a < b and li[b] > key:
            li[a] = li[b]
            a += 1
            li[b] = li[a]
    li[a] = key
    return a


def quick_sort(li, a, b):
    if a < b:
        middle = partiton(li, a, b)
        quick_sort(li, a, middle)
        quick_sort(li, middle+1, b)


def qs_blog(list):
    from routes.blog import Blog
    times = [x.created_time for x in list]
    print(times)
    quick_sort(times, 0, len(times)-1)
    return [Blog.find_by(created_time=x) for x in times]