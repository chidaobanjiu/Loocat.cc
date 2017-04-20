from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from models.todo import Todo
from utils import log


main = Blueprint('todo', __name__)


@main.route('/')
def index():
    todo_list = Todo.all()
    return render_template('todo_index.html', todos=todo_list)


@main.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == 'GET':
        return redirect(url_for('todo.index'))
    # request local
    # post form request.form()
    # get request.args
    form = request.form
    t = Todo.new(form)
    t.save()
    return redirect(url_for('todo.index'))


@main.route('/delete/<int:todo_id>/')
def delete(todo_id):
    t = Todo.delete(todo_id)
    log("deleted todo id", todo_id)
    return redirect(url_for('.index'))
