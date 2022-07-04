from flask import (
    Blueprint, current_app, jsonify, request
)
from bikemonitor.db import get_db
from math import sqrt

bp = Blueprint('data', __name__)

@bp.route("/data")
def data():
    #data = [{'points': [[53.519, -113.526], [53.525, -113.673]], 'color': '#663399'}]
    
    data = get_data(request.args)[0]
    return jsonify(data)

def get_data(args):
    print([i for i in args.items()])

    query_str = make_query_str(args)
    db = get_db()
    raw_data = db.execute(query_str, args)
    max_val = 25

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
    return data, max_val



def make_query_str(args):
    query = """SELECT g.lat1, g.lon1, g.lat2, g.lon2, b.avg_accel
    FROM (
    SELECT s.uid as uid, s.ts2 as ts2, AVG(z_accel * z_accel) as avg_accel
    FROM segments s, accelerometer a
    WHERE s.uid = a.user_id AND a.time_stamp <= s.ts2 and a.time_stamp >= s.ts1
    GROUP BY s.uid, s.ts2
    ) b, segments g
    WHERE g.uid = b.uid AND g.ts2 = b.ts2"""
    user_id = args.get("user_id", '')
    start_date = args.get("start_date", '')
    end_date = args.get("end_date", '')
    start_time = args.get("start_time", '')
    end_time = args.get("end_time", '')
    if user_id:
        query += " AND g.uid = :user_id"
    if start_date:
        query += " AND DATE(g.ts1 / 1000, 'unixepoch') >= :start_date"
    if end_date:
        query += " AND DATE(g.ts2 / 1000, 'unixepoch') <= :end_date"
    if start_time:
        query += " AND TIME(g.ts1 / 1000, 'unixepoch', 'localtime') >= TIME(:start_time)"
    if end_time:
        query += " AND TIME(g.ts2 / 1000, 'unixepoch', 'localtime') <= TIME(:end_time)"
    print(query)
    return query
