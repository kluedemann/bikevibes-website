import functools

from flask import (
    Blueprint, flash, g, jsonify, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from bike_monitor.db import get_db


bp = Blueprint('upload', __name__, url_prefix='/upload')


@bp.route("/location", methods=('POST'))
def location():
    user_id = request.args.get('user_id')
    trip_id = request.args.get('trip_id')
    timestamp = request.args.get('timestamp')
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')

    db = get_db()

    try:
        db.execute(
            "INSERT INTO locations (user_id, time_stamp, trip_id, latitude, longitude) VALUES (?, ?, ?, ?, ?)",
            (user_id, timestamp, trip_id, latitude, longitude),
        )
        db.commit()
    except db.IntegrityError:
        return jsonify(success=False), 500
    else:
        return jsonify(success=True) 
