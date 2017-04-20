from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    abort,
)
# 一次性引入多个 flask 里面的名字
# 注意最后一个后面也应该加上逗号
# 这样的好处是方便和一致性

from routes import current_user
from models.category import Category
from models.blog import Blog

import os
from werkzeug.utils import secure_filename
from config import user_file_director
from utils import qs_blog

import uuid
csrf_tokens = dict()

main = Blueprint('admin', __name__)


@main.route("/")
def index():
    if not current_user():
        print('admin index no user')
        abort(403)
    u = current_user()
    all_cats = Category.cache_all()
    all_blog = Blog.cache_all()

    token = str(uuid.uuid4())
    csrf_tokens[token] = u.id

    if len(all_blog) > 6:
        l = len(all_blog)
        blogs = all_blog[:6]
        blog_next = 6
    else:
        blog_next=None
        blogs = all_blog

    return render_template("admin/index.html", cats=all_cats, blogs=blogs, token=token, next=blog_next)


@main.route("/start<int:start_id>")
def start(start_id):
    u = current_user()
    all_cats = Category.cache_all()
    all_blog = Blog.cache_all()
    s = start_id

    token = str(uuid.uuid4())
    csrf_tokens[token] = u.id

    blogs = all_blog[s:]
    if len(blogs) <= 6:
        blog_prev = s - 6
        blog_next = None
    else:
        blogs = blogs[:6]
        blog_prev = s - 6
        blog_next = blog_prev + 12
        if blog_next > len(all_blog):
            blog_next = None

    return render_template("admin/index.html", blogs=blogs, cats=all_cats, prev=blog_prev, next=blog_next)


def allow_file(filename):
    suffix = filename.split('.')[-1]
    from config import accept_user_file_type
    return suffix in accept_user_file_type


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    Category.new(form)
    Category.should_update_all = True
    return redirect(url_for('.index'))


@main.route("/addimg<int:cat_id>", methods=["POST"])
def addimg(cat_id):
    c = Category.find(cat_id)

    if c is None:
        return redirect(url_for(".view", cat_id=cat_id))

    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    if allow_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(user_file_director, filename))
        c.image = filename
        c.save()

    return redirect(url_for(".index", cat_id=cat_id))


@main.route("/new")
def new():
    return render_template("admin/new.html")


@main.route("/edit<int:cat_id>")
def edit(cat_id):
    u = current_user()
    token = str(uuid.uuid4())
    csrf_tokens[token] = u.id
    print('edit add token', csrf_tokens)
    if current_user():
        cat = Category.find(cat_id)
        return render_template("admin/edit.html", cat=cat, token=token)
    else:
        abort(403)


@main.route("/edit_commit<int:cat_id>", methods=["POST"])
def change(cat_id):
    u = current_user()
    token = request.args.get('token')
    cat = Category.find(cat_id)
    form = request.form
    print('change token', token)
    print('csrf', csrf_tokens)
    print('u.id', u.id)
    print('token in csrf_tokens', token in csrf_tokens)
    print('csrf_tokens[token] == u.id', csrf_tokens[token] == u.id)
    if token in csrf_tokens and csrf_tokens[token] == u.id:
        cat.update(form)
        csrf_tokens.pop(token)
        Category.should_update_all = True
        cat.save()
        return redirect(url_for(".index", cat_id=cat.id))
    else:
        abort(403)


@main.route("/delete<int:blog_id>")
def deleteblog(blog_id):
    u = current_user()
    token = request.args.get('token')
    if token in csrf_tokens and csrf_tokens[token] == u.id:
        csrf_tokens.pop(token)
        Blog.should_update_all = True
        b = Blog.find(blog_id)
        b.delete()
        return redirect(url_for(".index"))
    else:
        abort(403)