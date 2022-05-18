import functools

from flask import (
    Blueprint, flash, g, jsonify, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from bikemonitor.db import get_db


bp = Blueprint('upload', __name__, url_prefix='/upload')


@bp.route("/location", methods=('POST',))
def location():
    db = get_db()

    try:
        db.execute(
            "INSERT INTO locations (user_id, time_stamp, trip_id, latitude, longitude)"
            " VALUES (:user_id, :time_stamp, :trip_id, :latitude, :longitude)",
            request.values,
        )
        db.commit()
    except db.IntegrityError:
        resp = jsonify(success=False)
        resp.status_code = 500
        return resp
    else:
        return jsonify(success=True) 


@bp.route("/accelerometer", methods=('POST',))
def accelerometer():
    db = get_db()

    try:
        db.execute(
            "INSERT INTO accelerometer (user_id, time_stamp, trip_id, x_accel, y_accel, z_accel)"
            " VALUES (:user_id, :time_stamp, :trip_id, :x_accel, :y_accel, :z_accel)",
            request.values,
        )
        db.commit()
    except db.IntegrityError:
        resp = jsonify(success=False)
        resp.status_code = 500
        return resp
    else:
        return jsonify(success=True) 