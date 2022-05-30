from flask import (
    Blueprint, render_template
)
from bikemonitor.db import get_db
from math import sqrt

bp = Blueprint('map', __name__)

@bp.route("/")
def index():
    db = get_db()
    with bp.open_resource('query.sql') as f:
        raw_data = db.execute(f.read().decode('utf8'))
    
    data = []
    max = 20
    for row in raw_data:
        average = min(sqrt(row[4]), max)
        color = int(average * 510 // max)
        red = 255
        green = 255
        if (color > 255):
            green = 510 - color
        else:
            red = color
        # print(average, color, red, green)
        data.append({'points': [row[0:2], row[2:4]], 'color': f'#{red:02X}{green:02X}00'})



    # db = get_db()
    # raw_data = db.execute('SELECT user_id, time_stamp, trip_id, latitude, longitude FROM locations ORDER BY user_id, time_stamp;').fetchall()
    
    # data = []
    # current = raw_data[0]
    # for i in range(1, len(raw_data)):
    #     prev = current
    #     current = raw_data[i]
    #     if (current[0] == prev[0] and current[2] == prev[2]):
    #         average = db.execute(
    #             "SELECT AVG(x_accel * x_accel + y_accel * y_accel + z_accel * z_accel) FROM accelerometer WHERE user_id=? AND time_stamp<=? AND time_stamp>=?", 
    #             [current[0], current[1], prev[1]]
    #         ).fetchone()[0]
    #         if (average is not None):
    #             average = min(sqrt(average), 20)
    #             color = int(average * 510 // 20)
    #             red = 255
    #             green = 255
    #             if (color > 255):
    #                 green = 510 - color
    #             else:
    #                 red = 510 - color
    #             # print(average, color, red, green)
    #             data.append({'points': [prev[3:5], current[3:5]], 'color': f'#{red:02X}{green:02X}00'})

    return render_template("index.html", data=data, max=f"{max:.1f}", hm=f"{max/2:.1f}")

