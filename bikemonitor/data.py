from flask import (
    Blueprint, current_app, jsonify, request
)
from bikemonitor.db import get_db
from math import log, sqrt


bp = Blueprint('data', __name__)


@bp.route("/data")
def data():   
    """
    Return json data with information used to update the map

    Returns:
        data - (dict) contains labelled information for the client
            lines - (list) the information needed to construct the polylines
                - each line contains two points and a color string
            max - (str) represents the maximum value on the color bar
            half - (str) represents the halfway value on the color bar
            center - (list) the lat-long coordinates of the center of the map
            zoom - (int) the zoom level of the map
    """

    # Query the values
    lines, max_val = get_data(request.args)
    max_str, max_hlf_str = get_strings(max_val)
    center, zoom = get_map(lines)

    data = {
        "lines": lines,
        "max": max_str,
        "half": max_hlf_str,
        "center": center,
        "zoom": zoom
    }

    return jsonify(data)


def get_map(lines):
    """
    Determine the new center and zoom level for the map

    Returns:
        center - (list) the lat-long coordinates of the new center point
            - calculated as the average of the min and max coordinates
        zoom - (int) the new zoom level of the map
            - calculated as the maximum zoom level that fits all segments into one tile
            then adds a constant adjustment
    """

    # Return default values if empty
    if not lines:
        return [53.5351, -113.4938], 12
    
    # Get the minimum and maximum coordinates
    min_lat = min(line['points'][0][0] for line in lines)
    max_lat = max(line['points'][0][0] for line in lines)
    min_lon = min(line['points'][0][1] for line in lines)
    max_lon = max(line['points'][0][1] for line in lines)

    # Calculate the center and zoom level
    center = [(min_lat + max_lat) / 2, (min_lon + max_lon) / 2]
    zoom_lat = min(int(-log((max_lat - min_lat) / 180, 2) + 1.5), 20)
    zoom_lon = min(int(-log((max_lon - min_lon) / 360, 2) + 1.5), 20)
    zoom = min(zoom_lat, zoom_lon)

    return center, zoom


def get_strings(max_val):
    """
    Construct the maximum and halfway strings for the color bar

    Returns:
        max_str - (str) the value to be displayed at the end of the color bar
        max_hlf_str - (str) the value to the displayed at the midpoint of the color bar
    """

    if max_val != 0:
        max_str = f"{max_val:.1f}"
        max_hlf_str = f"{max_val/2:.1f}"
    else:
        max_hlf_str="n/a"
        max_str="n/a"

    return max_str, max_hlf_str


def get_data(args):
    """Query the data from the database and construct it into lines.
    
    Returns:
        data - (list) used to construct the polylines for the map
            - each line contains two points and a color string
        max_val - (float) the maximum RMS of acceleration over the data
    """

    # Query data from database
    query_str = make_query_str(args)
    db = get_db()
    raw_data = db.execute(query_str, args).fetchall()

    # Determine maximum value
    max_val = 0
    if raw_data:
        max_val = sqrt(max(row[4] for row in raw_data))

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
    """Construct the query string from the form arguments delivered.
    
    Returns:
        query - (str) the query string to retrieve the segments
            - has additional constraints depending on the parameters given
    """

    query = """SELECT g.lat1, g.lon1, g.lat2, g.lon2, b.avg_accel
    FROM (
    SELECT s.uid as uid, s.ts2 as ts2, AVG(z_accel * z_accel) as avg_accel
    FROM segments s, accelerometer a
    WHERE s.uid = a.user_id AND a.time_stamp <= s.ts2 and a.time_stamp >= s.ts1
    GROUP BY s.uid, s.ts2
    ) b, segments g
    WHERE g.uid = b.uid AND g.ts2 = b.ts2"""
    
    if args.get("user_id", ''):
        query += " AND g.uid = :user_id"
    if args.get("start_date", ''):
        query += " AND DATE(g.ts1 / 1000, 'unixepoch') >= :start_date"
    if args.get("end_date", ''):
        query += " AND DATE(g.ts2 / 1000, 'unixepoch') <= :end_date"
    if args.get("start_time", ''):
        query += " AND TIME(g.ts1 / 1000, 'unixepoch', 'localtime') >= TIME(:start_time)"
    if args.get("end_time", ''):
        query += " AND TIME(g.ts2 / 1000, 'unixepoch', 'localtime') <= TIME(:end_time)"
    
    return query
