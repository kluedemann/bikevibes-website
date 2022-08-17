from flask import (
    Blueprint, request, jsonify, copy_current_request_context, current_app
)
from threading import Thread
from bikemonitor.db import get_db


bp = Blueprint('upload', __name__, url_prefix='/upload')


@bp.route("", methods=('POST',))
def upload():
    if request.is_json:
        data = request.json
        insert_data(data)
        return jsonify(success=True), 200
    else:
        return jsonify(success=False), 400


def insert_data(data):
    db = get_db()
    user_id = data["user_id"]
    db.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    
    queries = {
        'accelerometer': """
            INSERT OR IGNORE INTO accelerometer (user_id, time_stamp, trip_id, x_accel, y_accel, z_accel)
            VALUES (:user_id, :time_stamp, :trip_id, :x_accel, :y_accel, :z_accel)
        """,
        'locations': """
            INSERT OR IGNORE INTO locations (user_id, time_stamp, trip_id, latitude, longitude)
            VALUES (:user_id, :time_stamp, :trip_id, :latitude, :longitude)
        """,
        'surfaces': """
            INSERT OR IGNORE INTO surfaces (user_id, trip_id, surface)
            VALUES (:user_id, :trip_id, :surface)
        """
    }
    for datatype in queries:
        insert_records(user_id, data[datatype], queries[datatype])
    db.commit()


def insert_records(user_id, data, query):
    for record in data:
        record["user_id"] = user_id
    db = get_db()
    db.executemany(query, data)


@bp.route("/location", methods=('POST',))
def location():
    """Upload an location record to the database.
    
    Query Parameters:
        user_id (str) - the user that the record belongs to
        time_stamp (long) - the unix timestamp of the record in ms
        latitude (double) - the latitude recorded
        longitude (double) - the longitude recorded

    Returns: a JSON object indicating success
    """

    query = """
    INSERT INTO locations (user_id, time_stamp, trip_id, latitude, longitude)
     VALUES (:user_id, :time_stamp, :trip_id, :latitude, :longitude)
    """

    return insert_query(query, request.values)


@bp.route("/accelerometer", methods=('POST',))
def accelerometer():
    """Upload an accelerometer record to the database.
    
    Query Parameters:
        user_id (str) - the user that the record belongs to
        time_stamp (long) - the unix timestamp of the record in ms
        x_accel (float) - the instantaneous x acceleration
        y_accel (float) - the instantaneous y acceleration
        z_accel (float) - the instantaneous z acceleration

    Returns: a JSON response indicating success
    """

    query = """
    INSERT INTO accelerometer (user_id, time_stamp, trip_id, x_accel, y_accel, z_accel)
     VALUES (:user_id, :time_stamp, :trip_id, :x_accel, :y_accel, :z_accel)
    """

    return insert_query(query, request.values)


@bp.route("/alias", methods=('POST',))
def alias():
    """Upload an alias to the database.
    
    Query Parameters:
        user_id (str) - the user whose alias will be set
        alias (str) - the alias to give the user

    Returns: a JSON response indicating success 
    """

    query = """
    INSERT INTO users (user_id, alias) VALUES (:user_id, :alias)
     ON CONFLICT(user_id) DO UPDATE SET
     alias=excluded.alias WHERE user_id=excluded.user_id
    """

    args = dict(request.values)
    if 'alias' not in args:
        args['alias'] = None
    return insert_query(query, args)


@bp.route("/surface", methods=('POST',))
def surface():
    """Upload a trip surface into the database.
    
    Query Parameters:
        user_id (str) - the user who the trip belongs to
        trip_id (int) - the trip whose surface is classified
        surface (str) - the primary surface over which the trip took place

    Returns: a JSON response indicating success
    """

    query = """
    INSERT INTO surfaces (user_id, trip_id, surface)
     VALUES (:user_id, :trip_id, :surface)
    """
    args = dict(request.values)
    if 'surface' not in args:
        args['surface'] = None
    return insert_query(query, args)


def insert_query(query, args):
    """Execute an insertion query on the database.
    Returns a response indicating success with an appropriate status code.
    Uses 409 (conflict) for a database integrity error, 400 for missing arguments.
    
    Parameters:
        query (str) - the sqlite query to execute
        args (dict) - the keyword arguments for the sqlite query

    Returns: a JSON response indicating success
    """

    db = get_db()
    try:
        db.execute(query, args)
        db.commit()
    except db.IntegrityError:
        resp = jsonify(success=False)
        resp.status_code = 409
        return resp
    except db.ProgrammingError:
        resp = jsonify(success=False)
        resp.status_code = 400
        return resp
    else:
        return jsonify(success=True)
