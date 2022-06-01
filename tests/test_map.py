from bikemonitor.db import get_db, init_db


def test_index(client):
    # Test if map page loads
    response = client.get('/')
    assert response.status_code == 200
    assert b"BikeMonitor" in response.data


def test_query(app):
    # Test whether the queries work as intended
    with app.app_context():
        # Test averages of segments
        with app.open_resource('queries/avg_query.sql') as f:
            raw_data = get_db().execute(f.read().decode('utf8')).fetchall()
            assert len(raw_data) == 4
            assert list(raw_data[2]) == [53.5, -113.45, 53.52, -113.48, (-50) ** 2]
        
        # Test maximum of segment averages
        with app.open_resource('queries/max_query.sql') as f:
            max_val = get_db().execute(f.read().decode('utf8')).fetchone()[0]
            assert max_val == (-50) ** 2


def test_empty(app, client):
    # Test empty data
    with app.app_context():
        init_db()
    
    # Get response
    response = client.get('/')
    assert response.status_code == 200
    assert b"n/a" in response.data
