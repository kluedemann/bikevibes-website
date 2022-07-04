from flask import (
    Blueprint, current_app, render_template
)


bp = Blueprint('map', __name__)


@bp.route("/")
def index():
    # Get raw data
    return render_template("index.html", api_key=current_app.config['API_KEY'])
