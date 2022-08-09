from bikemonitor.db import get_db, init_db


def test_data(client):
    # Test the data routing

    # Ensure correct data is returned
    response = client.get('/data')
    data = response.json
    assert data['center'] == [53.535, -113.485]
    assert data['half'] == '1.8'
    assert data['max'] == '3.5'
    assert data['zoom'] == 12

    # Ensure line is calculated correctly
    lines = data['lines']
    assert len(lines) == 5
    assert lines[0]['color'] == '#FF0000'
    assert lines[0]['points'] == [[53.5, -113.45], [53.52, -113.48]]

    # Test empty data
    response = client.get('/data?alias=this+does+not+exist')
    data = response.json
    assert data['center'] == [53.5351, -113.4938]
    assert data['zoom'] == 12
    assert data['max'] == "3.5"
    assert data['half'] == "1.8"
    assert data['lines'] == []

    # Test desktop size
    response = client.get('/data?width=2000&height=2000')

    # Test query parameters
    response = client.get('/data?alias=apple&start_date=0000-01-01&end_date=2023-01-01&start_time=00:00&end_time=23:59&surface=Pavement')
    assert len(response.json['lines']) > 0

    response = client.get('/data?alias=point')
    data = response.json
    assert data['zoom'] == 20
