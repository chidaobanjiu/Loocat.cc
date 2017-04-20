from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)


main = Blueprint('map', __name__)


@main.route('/')
def index():
    return render_template('/map/map.html')



