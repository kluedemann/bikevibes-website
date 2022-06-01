from bikemonitor.db import get_db


def test_location(client, app):
    # Upload valid location
    response = client.post(
        '/upload/location', data={'user_id': 'a', 'time_stamp': 2000, 'trip_id': 2, 'latitude': 1.0, 'longitude': 1.0}
    )
    assert response.status_code == 200
    assert response.json["success"]

    # Check location exists
    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM locations WHERE user_id = 'a'",
        ).fetchone() is not None

    # Upload invalid location
    response = client.post(
        '/upload/location', data={'user_id': 'a', 'time_stamp': 2000, 'trip_id': 3, 'latitude': 2.0, 'longitude': 2.0}
    )
    assert response.status_code == 500
    assert not response.json["success"]


def test_accelerometer(client, app):
    # Upload valid accelerometer data
    response = client.post(
        '/upload/accelerometer', data={'user_id': 'a', 'time_stamp': 2000, 'trip_id': 2, 'x_accel': 1.0, 'y_accel': 0.0, 'z_accel': -1.0}
    )
    assert response.status_code == 200
    assert response.json["success"]

    # Check accelerometer data exists
    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM accelerometer WHERE user_id = 'a'",
        ).fetchone() is not None

    # Upload invalid accelerometer data
    response = client.post(
        '/upload/accelerometer', data={'user_id': 'a', 'time_stamp': 2000, 'trip_id': 3, 'x_accel': 2.0, 'y_accel': 10.0, 'z_accel': -2.0}
    )
    assert response.status_code == 500
    assert not response.json["success"]
