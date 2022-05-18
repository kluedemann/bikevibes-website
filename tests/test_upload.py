import pytest
from flask import g, session
from bikemonitor.db import get_db


def test_location(client, app):
    response = client.post(
        '/upload/location', data={'user_id': 'a', 'time_stamp': 2000, 'trip_id': 2, 'latitude': 1.0, 'longitude': 1.0}
    )
    assert response.status_code == 200

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM locations WHERE user_id = 'a'",
        ).fetchone() is not None

    response = client.post(
        '/upload/location', data={'user_id': 'a', 'time_stamp': 2000, 'trip_id': 3, 'latitude': 2.0, 'longitude': 2.0}
    )
    assert response.status_code == 500


def test_accelerometer(client, app):
    response = client.post(
        '/upload/accelerometer', data={'user_id': 'a', 'time_stamp': 2000, 'trip_id': 2, 'x_accel': 1.0, 'y_accel': 0.0, 'z_accel': -1.0}
    )
    assert response.status_code == 200

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM accelerometer WHERE user_id = 'a'",
        ).fetchone() is not None

    response = client.post(
        '/upload/accelerometer', data={'user_id': 'a', 'time_stamp': 2000, 'trip_id': 3, 'x_accel': 2.0, 'y_accel': 10.0, 'z_accel': -2.0}
    )
    assert response.status_code == 500
