from flask import (
    Blueprint, jsonify, request
)
from bikemonitor.db import get_db
from math import log, sqrt


bp = Blueprint('delete', __name__)


@bp.route("/delete/<string:user_id>", methods=('DELETE',))
def delete(user_id):
    db = get_db()
    db.execute("DELETE FROM accelerometer WHERE user_id=?", (user_id,))
    db.execute("DELETE FROM locations WHERE user_id=?", (user_id,))
    db.execute("DELETE FROM surfaces WHERE user_id=?", (user_id,))
    db.execute("DELETE FROM users WHERE user_id=?", (user_id,))
    db.commit()
    return jsonify(success=True)
