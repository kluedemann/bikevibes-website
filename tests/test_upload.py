from bikemonitor.db import get_db


def test_valid_upload(client):
    """Test whether invalid uploads are identified."""

    # Valid upload
    response = client.post('/upload', json={
        'user_id': 'c',
        'accelerometer': [],
        'locations': [],
        'surfaces': []
        })
    assert response.status_code == 200
    assert response.json["success"]

    # Valid: Omitted tables
    response = client.post('/upload', json={
        'user_id': 'c'
        })
    assert response.status_code == 200
    assert response.json["success"]

    # Invalid: Missing user
    response = client.post('/upload', json={
        'accelerometer': [],
        'locations': [],
        'surfaces': []
        })
    assert response.status_code == 400
    assert not response.json["success"]

    # Invalid: Not JSON
    response = client.post('/upload', data={
        'user_id': 'c',
        'accelerometer': [],
        'locations': [],
        'surfaces': []
        })
    assert response.status_code == 400
    assert not response.json["success"]

def test_insert(client, app):
    """Test whether data is correctly inserted."""

    # Upload data
    response = client.post('/upload', json={
        'user_id': 'upload-1',
        'accelerometer': [{
            'time_stamp': 0,
            'trip_id': 0,
            'x_accel': 0.0,
            'y_accel': 0.0,
            'z_accel': 0.0
        }],
        'locations': [{
            'time_stamp': 0,
            'trip_id': 0,
            'latitude': 0.0,
            'longitude': 0.0
        }],
        'surfaces': [{
            'trip_id': 0,
            'surface': 'Pavement'
        }]
    })
    assert response.status_code == 200
    assert response.json["success"]
    
    # Assert data was inserted
    with app.app_context():
        db = get_db()

        # Check user
        user = db.execute("SELECT * FROM users WHERE user_id='upload-1'").fetchone()
        assert tuple(user) == ('upload-1', None)

        # Check accelerometer
        accel = db.execute("SELECT * FROM accelerometer WHERE user_id='upload-1'").fetchone()
        assert tuple(accel) == ('upload-1', 0, 0, 0.0, 0.0, 0.0)

        # Check location
        location = db.execute("SELECT * FROM locations WHERE user_id='upload-1'").fetchone()
        assert tuple(location) == ('upload-1', 0, 0, 0.0, 0.0)

        # Check surface
        surface = db.execute("SELECT * FROM surfaces WHERE user_id='upload-1'").fetchone()
        assert tuple(surface) == ('upload-1', 0, 'Pavement')


def test_existing_user(client, app):
    """Ensure correct handling of existing user"""
    
    # Upload existing user
    response = client.post('/upload', json={
        'user_id': 'a',
        'accelerometer': [{
            'time_stamp': 0,
            'trip_id': 0,
            'x_accel': 0.0,
            'y_accel': 0.0,
            'z_accel': 0.0
        }],
        'locations': [{
            'time_stamp': 0,
            'trip_id': 0,
            'latitude': 0.0,
            'longitude': 0.0
        }],
        'surfaces': [{
            'trip_id': 0,
            'surface': 'Pavement'
        }]
    })
    assert response.status_code == 200
    assert response.json["success"]

    with app.app_context():
        db = get_db()

        # Ensure no users are added or updated
        users = db.execute("SELECT * FROM users WHERE user_id='a'").fetchall()
        assert len(users) == 1
        assert tuple(users[0]) == ('a', 'banana')

        # Check data uploaded
        assert db.execute("SELECT * FROM accelerometer WHERE user_id='a'").fetchone() is not None
        assert db.execute("SELECT * FROM locations WHERE user_id='a'").fetchone() is not None
        assert db.execute("SELECT * FROM surfaces WHERE user_id='a'").fetchone() is not None


def test_bad_record(client, app):
    """Ensure invalid JSON data objects are handled correctly"""

    # All bad requests
    response = client.post('/upload', json={
        'user_id': 'upload-2',
        'accelerometer': [{
            'trip_id': 0,
            'x_accel': 0.0,
            'y_accel': 0.0,
            'z_accel': 0.0
        }, {
            'time_stamp': 0,
            'trip_id': 0,
            'x_accel': 0.0,
            'y_accel': 0.0,
            'z_accel': 0.0
        }],
        'locations': [{
            'time_stamp': 0,
            'latitude': 0.0,
            'longitude': 0.0
        }, {
            'time_stamp': 1,
            'trip_id': 0,
            'latitude': 0.0,
            'longitude': 0.0
        }],
        'surfaces': [{
            'trip_id': 0,
        }, {
            'trip_id': 1,
            'surface': 'Pavement'
        }]
    })
    assert response.status_code == 400
    assert not response.json["success"]

    # Assert no values inserted
    with app.app_context():
        db = get_db()
        assert db.execute("SELECT * FROM accelerometer WHERE user_id='upload-2'").fetchone() is None
        assert db.execute("SELECT * FROM locations WHERE user_id='upload-2'").fetchone() is None
        assert db.execute("SELECT * FROM surfaces WHERE user_id='upload-2'").fetchone() is None

    # Ensure other queries are still run despite error returned
    response = client.post('/upload', json={
        'user_id': 'upload-3',
        'accelerometer': [{}],
        'locations': [{
            'time_stamp': 0,
            'trip_id': 0,
            'latitude': 0.0,
            'longitude': 0.0
        }]
    })
    assert response.status_code == 400
    assert not response.json["success"]

    # Assert location inserted
    with app.app_context():
        db = get_db()
        assert db.execute("SELECT * FROM locations WHERE user_id='upload-3'").fetchone() is not None


# TODO: Write test for duplicate inserts

############################# Legacy Methods ########################################

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
