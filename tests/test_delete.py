from bikemonitor.db import get_db, init_db


def test_delete(client, app):
    # Delete user
    response = client.delete("/delete/test3")
    assert response.status_code == 200
    assert response.json["success"]

    # Check that only the user was deleted
    with app.app_context():
        data = get_db().execute("SELECT user_id FROM locations").fetchall()
        assert len(data) == 10
        assert 'test3' not in data

        data = get_db().execute("SELECT user_id FROM accelerometer").fetchall()
        assert len(data) == 6
        assert 'test3' not in data

        data = get_db().execute("SELECT user_id FROM surfaces").fetchall()
        assert len(data) == 5
        assert 'test3' not in data

        data = get_db().execute("SELECT user_id FROM users").fetchall()
        assert len(data) == 3
        assert 'test3' not in data

        
        