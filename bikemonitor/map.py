from flask import (
    Blueprint, current_app, render_template
)
from bikemonitor.db import get_db
from math import sqrt


bp = Blueprint('map', __name__)


@bp.route("/")
def index():
    # Get raw data
    db = get_db()
    with bp.open_resource('queries/avg_query.sql') as f:
        raw_data = db.execute(f.read().decode('utf8'))
    
    # Get maximum value
    # with bp.open_resource('queries/max_query.sql') as f:
    #     max_val = db.execute(f.read().decode('utf8')).fetchone()[0]
    max_val = 25

    # Handle empty result set
    if max_val is not None:
        max_val = sqrt(max_val)
        max_str = f"{max_val:.1f}"
        max_hlf_str = f"{max_val/2:.1f}"
    else:
        max_str = "n/a"
        max_hlf_str = "n/a"
    
    data = []
    for row in raw_data:
        # Calculate color values
        average = min(sqrt(row[4]), max_val)
        color = int(average * 510 // max_val)
        red = 255
        green = 255
        if (color > 255):
            green = 510 - color
        else:
            red = color

        # print(average, color, red, green)
        data.append({'points': [row[0:2], row[2:4]], 'color': f'#{red:02X}{green:02X}00'})

    return render_template("index.html", data=data, max=max_str, hm=max_hlf_str, api_key=current_app.config['API_KEY'])
