from flask import (
    Blueprint, jsonify, request
)
from bikemonitor.db import get_db
from math import log, sqrt


bp = Blueprint('data', __name__)


@bp.route("/data")
def data():   
    """
    Return json data with information used to update the map

    Query Parameters:
        alias (str) - the alias to search for
        start_date (str) - the start date in YYYY-MM-DD format
        end_date (str) - the end date in YYYY-MM-DD format
        start_time (str) - the start time in HH:mm format
        end_time (str) - the end time in HH:mm format
        width (int) - the viewport width in pixels
        height (int) - the viewport height in pixels

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
    lines, max_val = get_data(request.values)
    max_str, max_hlf_str = get_strings(max_val)
    width = int(request.values.get("width", 400))
    height = int(request.values.get("height", 800))
    center, zoom = get_map(lines, width, height)

    data = {
        "lines": lines,
        "max": max_str,
        "half": max_hlf_str,
        "center": center,
        "zoom": zoom
    }

    return jsonify(data)


def get_map(lines, width, height):
    """
    Determine the new center and zoom level for the map.

    Parameters:
        lines - (list) the list of polylines stored in dicts as a list of points and a color string
        width - (int) the width of the viewport in pixels
        height - (int) the height of the viewport in pixels

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
    first_lat = lines[0]['points'][0][0]
    first_lon = lines[0]['points'][0][1]
    min_lat = min(min(line['points'][1][0] for line in lines), first_lat)
    max_lat = max(max(line['points'][1][0] for line in lines), first_lat)
    min_lon = min(min(line['points'][1][1] for line in lines), first_lon)
    max_lon = max(max(line['points'][1][1] for line in lines), first_lon)

    # Account for map being part of the screen
    if width >= 768:
        width = width * 4 // 5
    else:
        height = height * 65 // 100

    # Calculate the center and zoom level
    center = [(min_lat + max_lat) / 2, (min_lon + max_lon) / 2]

    if max_lat != min_lat and height != 0: 
        zoom_lat = min(int(-log((max_lat - min_lat) * 256 / (180 * height), 2)), 20)
    else:
        zoom_lat = 20

    if max_lon != min_lon and width != 0:
        zoom_lon = min(int(-log((max_lon - min_lon) * 256 / (360 * width), 2)), 20)
    else:
        zoom_lon = 20

    zoom = min(zoom_lat, zoom_lon)
    return center, zoom


def get_strings(max_val):
    """
    Construct the maximum and halfway strings for the color bar

    Parameters:
        max_val - (float) the maximum value returned by the query

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
    """
    Query the data from the database and construct it into lines.

    Parameters:
        args - (ImmutibleMultiDict) the parameters received in the HTTP request
    
    Returns:
        data - (list) used to construct the polylines for the map
            - each line contains two points and a color string
        max_val - (float) the maximum RMS of acceleration over the data
    """

    # Query data from database
    db = get_db()
    query_str = make_query_str(args)
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
    """
    Construct the query string from the form arguments delivered.
    
    Parameters:
        args - (dict) the parameters in the HTTP request to filter with

    Returns:
        query - (str) the query string to retrieve the segments
            - has additional constraints depending on the parameters given
    """

    query = """
    SELECT g.lat1, g.lon1, g.lat2, g.lon2, b.avg_accel
    FROM (
    SELECT s.uid as uid, s.ts2 as ts2, AVG(z_accel * z_accel) as avg_accel
    FROM segments s, accelerometer a
    WHERE s.uid = a.user_id AND a.time_stamp <= s.ts2 and a.time_stamp >= s.ts1
    GROUP BY s.uid, s.ts2
    ) b, segments g
    """
    where_clause = " WHERE g.uid = b.uid AND g.ts2 = b.ts2"

    # Determine row limit
    LIMIT_AMOUNT = 20000
    is_mobile = (int(args.get("width", 0)) < 1300) and (int(args.get("height", 0)) < 1300)
    if is_mobile:
        LIMIT_AMOUNT = 2000
    
    # Add query filters
    if args.get("alias", ''):
        query += ", users u" + where_clause + " AND u.alias = :alias AND g.uid = u.user_id"
    else:
        query += where_clause
    if args.get("start_date", ''):
        query += " AND DATE(g.ts1 / 1000, 'unixepoch', '-6 hours') >= :start_date"
    if args.get("end_date", ''):
        query += " AND DATE(g.ts2 / 1000, 'unixepoch', '-6 hours') <= :end_date"
    if args.get("start_time", ''):
        query += " AND TIME(g.ts1 / 1000, 'unixepoch', '-6 hours') >= TIME(:start_time)"
    if args.get("end_time", ''):
        query += " AND TIME(g.ts2 / 1000, 'unixepoch', '-6 hours') <= TIME(:end_time)"

    # Add row limit
    query += f" ORDER BY g.ts1 DESC LIMIT {LIMIT_AMOUNT}"
    return query
