from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    send_from_directory,
    abort,
)

from models.blog import (
    Blog,
    BlogComment,
)
from models.category import Category

import os
from werkzeug.utils import secure_filename
from config import user_file_director
from routes import *
from utils import qs_blog

# 防范 xsrf
import uuid
csrf_tokens = dict()

main = Blueprint('blog', __name__)


# def allow_file(filename):
#     suffix = filename.split('.')[-1]
#     from config import accept_user_file_type
#     return suffix in accept_user_file_type


@main.route("/")
def index():
    all_blog = qs_blog(Blog.cache_all())
    all_cat = Category.cache_all()
    u = current_user()

    if len(all_blog) > 6:
        l = len(all_blog)
        blogs = all_blog[:6]
        blog_next = 6
    else:
        blog_next=None
        blogs = all_blog

    return render_template("blog/index.html", blogs=blogs, cats=all_cat, next=blog_next, user=u)


@main.route("/start<int:start_id>")
def start(start_id):
    all_blog = qs_blog(Blog.cache_all())
    all_cat = Category.cache_all()
    s = start_id

    blogs=all_blog[s:]
    if len(blogs) <= 6:
        blog_prev = s - 6
        blog_next = None
    else:
        blogs = blogs[:6]
        blog_prev = s - 6
        blog_next = blog_prev + 12
        if blog_next > len(all_blog):
            blog_next = None

    return render_template("blog/index.html", blogs=blogs, cats=all_cat, prev=blog_prev, next=blog_next)


@main.route("/archive")
def archive():
    all_blog = Blog.cache_all()
    return render_template("blog/archive.html", blogs=all_blog)


@main.route("/blogs_in_<int:category_id>")
def blogsincat(category_id):
    u = current_user()
    cat = Category.find_by(id=category_id)
    all_blog = qs_blog(cat.blogs())
    all_cat = Category.cache_all()
    # return render_template("blog/index.html", blogs=all_blog)
    return render_template("blog/index.html", blogs=all_blog, cat=cat, cats=all_cat, user=u)


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    b = Blog.new(form)
    Blog.should_update_all = True
    return redirect(url_for('.index'))


# @main.route("/addimg<blog_id>", methods=["POST"])
# def addimg(blog_id):
#     b = Blog.find(blog_id)
#
#     if b is None:
#         return redirect(url_for(".view", blog_id=blog_id))
#
#     if 'file' not in request.files:
#         return redirect(request.url)
#
#     file = request.files['file']
#     if file.filename == '':
#         return redirect(request.url)
#
#     if allow_file(file.filename):
#         filename = secure_filename(file.filename)
#         file.save(os.path.join(user_file_director, filename))
#         b.image = filename
#         b.save()
#
#     return redirect(url_for(".view", blog_id=blog_id))


@main.route("/new")
def new():
    all_cat = Category.cache_all()
    u = current_user()
    if current_user():
        return render_template("blog/new.html", cats=all_cat, u=u)
    else:
        abort(403)


# /blog/1
@main.route("/blog-<int:blog_id>")
def view(blog_id):
    u = current_user()
    # comments = BlogComment.find_all(blog_id=blog_id)
    blog = Blog.find(blog_id)
    cat = Category.find(blog.category)
    if Blog.find(blog_id+1):
        next_blog = Blog.find(blog_id+1)
    else:
        next_blog = Blog.cache_all()[0]
    return render_template("blog/view.html", blog=blog, nxblog=next_blog, user=u, cat=cat)


@main.route("/edit<int:blog_id>")
def edit(blog_id):
    u = current_user()
    token = str(uuid.uuid4())
    csrf_tokens[token] = u.id
    # print('edit add token', csrf_tokens)
    if current_user():
        blog = Blog.find(blog_id)
        cat = Category.find(blog.category)
        cats = Category.cache_all()
        return render_template("blog/edit.html", blog=blog, cats=cats, cat=cat, u=u, token=token)
    else:
        abort(403)


@main.route("/edit_commit<int:blog_id>", methods=["POST"])
def change(blog_id):
    u = current_user()
    blog = Blog.find(blog_id)
    form = request.form
    token = request.args.get('token')
    # <a class="next__link" href="url_for('.view', blog_id=blog.id)" style="background-image: url('https://unsplash.it/2000/1200?image=855');">int('u.id', u.id)
    # print('before update', type(Blog.find(blog_id).admin))
    # print('form', type(form.get('admin')))
    if token in csrf_tokens and csrf_tokens[token] == u.id:
        csrf_tokens.pop(token)
        Blog.should_update_all = True
        blog.update(form)
        c = form.get('category')
        blog.category = int(c)
        # print('after update', type(Blog.find(blog_id).admin))
        cat = Category.find(blog.category)
        blog.save()
        return redirect(url_for(".view", blog_id=blog.id, cat=cat))
    else:
        abort(403)


@main.route("/comment/new", methods=["POST"])
def comment():
    form = request.form
    BlogComment.new(form)
    return redirect(url_for('.view', blog_id=form.get("blog_id")))


@main.route("/uploads/<filename>")
def uploads(filename):
    return send_from_directory(user_file_director, filename)


@main.route("/Benjamin Jiang")
def profile():
    return render_template('/blog/profile.html')
