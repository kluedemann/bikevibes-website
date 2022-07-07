def test_index(client):
    # Test if map page loads
    response = client.get('/')
    assert response.status_code == 200
    assert b"BikeVibes" in response.data
    assert b"n/a" in response.data
    assert b'href="https://www.bikevibes.ca"' in response.data
    assert b'href="https://forms.gle/EpxfVKBe8BqUsJFo8"' in response.data
