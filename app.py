from flask import Flask
from utils import (
    datetimeformat,
    abstract,
)

from routes.map import main as map_routes
from routes.blog import main as blog_routes
from routes.todo import main as todo_routes
from routes.admin import main as admin_routes
from routes.index import main as index_routes
from routes.comment import main as comment_routes

app = Flask(__name__)
app.secret_key = 'secret not secret'

app.register_blueprint(map_routes, url_prefix='/map')
app.register_blueprint(blog_routes, url_prefix='/blog')
app.register_blueprint(todo_routes, url_prefix='/todo')
app.register_blueprint(admin_routes, url_prefix='/admin')
app.register_blueprint(comment_routes, url_prefix='/comment')
app.register_blueprint(index_routes)


app.jinja_env.filters['datetime'] = datetimeformat
app.jinja_env.filters['abstract'] = abstract


if __name__ == '__main__':
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=2001,
    )
    app.run(**config)
