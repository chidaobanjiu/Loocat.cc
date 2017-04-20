from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    make_response,
)
from models.user import User
from utils import log

main = Blueprint('index', __name__)


def current_user():
    uid = session.get('user_id', -1)
    u = User.find_by(id=uid)
    return u


@main.route("/")
def index():
    u = current_user()
    template = render_template("index.html", user=u)
    r = make_response(template)
    r.set_cookie('cookie_name', 'GUA')
    return r


@main.route("/register", methods=['POST'])
def register():
    form = request.form
    u = User.register(form)
    return redirect(url_for('.index'))


@main.route("/login", methods=['POST'])
def login():
    form = request.form
    u = User.validate_login(form)
    if u is None:
        return redirect(url_for('.index'))
    else:
        # session 中写入 user_id
        session['user_id'] = u.id
        return redirect(url_for('blog.index'))


@main.route("/visit")
def visit():
    u = current_user()
    session['user_id'] = -1
    return redirect(url_for('blog.index'))


@main.route("/logout", methods=['get'])
def log_out():
    session.pop("user_name")
    return redirect(url_for(".index"))


# @main.route('/profile')
# def profile():
#     u = current_user()
#     if u is None:
#         return redirect(url_for('.index'))
#     else:
#         return render_template('profile.html', user=u)
