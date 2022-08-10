from bikemonitor.db import get_db


def test_location(client, app):
    """Test uploading a location to the database."""

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
    assert response.status_code == 409
    assert not response.json["success"]

    # Upload empty data
    response = client.post('/upload/location')
    assert response.status_code == 400
    assert not response.json["success"]


def test_accelerometer(client, app):
    """Test uploading an accelerometer record to the database."""

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
    assert response.status_code == 409
    assert not response.json["success"]

    # Upload empty data
    response = client.post('/upload/accelerometer')
    assert response.status_code == 400
    assert not response.json["success"]


def test_alias(client, app):
    """Test uploading an alias to the database."""

    # Upload a valid alias
    response = client.post(
        '/upload/alias', data={'user_id': 'b', 'alias': 'test alias'}
    )
    assert response.status_code == 200
    assert response.json["success"]

    # Upload an empty alias
    response = client.post(
        '/upload/alias?user_id=new'
    )
    assert response.status_code == 200
    assert response.json["success"]

    # Update an existing alias
    response = client.post(
        '/upload/alias', data={'user_id': 'test', 'alias': 'pear'}
    )
    assert response.status_code == 200
    assert response.json["success"]

    # Check accelerometer data exists
    with app.app_context():
        data = get_db().execute(
            "SELECT * FROM users",
        ).fetchall()
        assert len(data) == 6


    # Upload a conflicting alias
    response = client.post(
        '/upload/alias', data={'user_id': 'd', 'alias': 'pear'}
    )
    assert response.status_code == 409
    assert not response.json["success"]

    # Upload empty data
    response = client.post('/upload/alias')
    assert response.status_code == 400
    assert not response.json["success"]

def test_surface(client, app):
    """Test uploading a surface to the database."""

    # Upload a surface record
    response = client.post(
        '/upload/surface', data={'user_id': 'a', 'trip_id': 2, 'surface': 'Dirt'}
    )
    assert response.status_code == 200
    assert response.json["success"]

    # Upload for another trip
    response = client.post(
        '/upload/surface', data={'user_id': 'a', 'trip_id': 3}
    )
    assert response.status_code == 200
    assert response.json["success"]

    # Check surface data exists
    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM surfaces WHERE user_id = 'a'",
        ).fetchone() is not None

    # Upload conflicting surface
    response = client.post(
        '/upload/surface', data={'user_id': 'a', 'trip_id': 2, 'surface': 'Gravel'}
    )
    assert response.status_code == 409
    assert not response.json["success"]

    # Upload empty data
    response = client.post('/upload/surface')
    assert response.status_code == 400
    assert not response.json["success"]
