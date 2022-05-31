from bikemonitor.db import get_db


def test_index(client):
    # Test if map page loads
    response = client.get('/')
    assert response.status_code == 200
    assert b"BikeMonitor" in response.data


def test_query(app):
    # Test whether the query
    with app.app_context():
        with app.open_resource('queries/avg_query.sql') as f:
            raw_data = get_db().execute(f.read().decode('utf8')).fetchall()
            assert len(raw_data) == 4
            assert list(raw_data[0]) == [53.5, -113.45, 53.52, -113.48, 3 * ((-50) ** 2)]
        with app.open_resource('queries/max_query.sql') as f:
            max_val = get_db().execute(f.read().decode('utf8')).fetchone()[0]
            assert max_val == 3 * ((-50) ** 2)
