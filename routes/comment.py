from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)
# 一次性引入多个 flask 里面的名字
# 注意最后一个后面也应该加上逗号
# 这样的好处是方便和一致性

from models.comment import Comment
from utils import log


main = Blueprint('comment', __name__)

'''
1. 拆分有哪些页面 一个页面就可以了，
---author---content----button---

-- comment---
-- comment---
。。。。。

2. 组织那些数据，把数据的操作实现
comment 数据结构
1. id
2. author String
3. content String
4. time int

comment 的数据上的方法
1. 新建评论
2. 所有的评论

数据结构 + 数据方法 类

3. 逻辑 产品经理
    3.1 add时候增加一个评论，然后跳转回到主页，在主页显示所有的评论
4. 开始实现代码，部分对，部分todo 开发工程师 测试工程师
5. 剩下的部分一点点补全
6. 美化页面 视觉
7. 交互细节 交互
'''

'''
1. tcp byte 数据流
2. http 严格要求了， request response // 发送给web framework什么？
    in： 已经parse过的request
    out: response writer
2.* 对于web framework 我看起来像是一个http server
    对于http server，我看起来像是一个web framework

    1. session sessionmiddlewareinterface
    2. cache memcached
3. web framework, flask
    3.1 M mongo redis mysql
    3.2 V jinja2
    3.3 C route
4. application
'''


@main.route('/')
def index():
    comments = Comment.all()
    return render_template('comment_new.html', comments=comments)


@main.route('/add', methods=['POST'])
def add():
    t = Comment.new(request.form)
    #t.save()
    return redirect(url_for('.index'))