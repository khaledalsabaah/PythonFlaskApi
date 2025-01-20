from unittest.mock import patch, MagicMock
import pytest
from app_package import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch('app_package.app.get_db_connection')
def test_health_endpoint(mock_db_conn, client):
    """Test the /health endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == "Up & Running"

@patch('app_package.app.get_db_connection')
def test_create_table_endpoint(mock_db_conn, client):
    """Test the /create_table endpoint."""
    mock_connection = MagicMock()
    mock_db_conn.return_value = mock_connection
    response = client.get('/create_table')
    assert response.status_code == 200
    assert "Table created successfully" in response.data.decode('utf-8')

@patch('app_package.app.get_db_connection')
def test_insert_record_endpoint(mock_db_conn, client):
    """Test the /insert_record endpoint."""
    mock_connection = MagicMock()
    mock_db_conn.return_value = mock_connection
    mock_cursor = mock_connection.cursor.return_value
    response = client.post('/insert_record', json={'name': 'John Doe'})
    assert response.status_code == 200
    assert "Record inserted successfully" in response.data.decode('utf-8')
    mock_cursor.execute.assert_called_once_with(
        "INSERT INTO example_table (name) VALUES (%s)", ('John Doe',)
    )

@patch('app_package.app.get_db_connection')
def test_data_endpoint(mock_db_conn, client):
    """Test the /data endpoint."""
    mock_connection = MagicMock()
    mock_db_conn.return_value = mock_connection
    mock_cursor = mock_connection.cursor.return_value
    mock_cursor.fetchall.return_value = [{'id': 1, 'name': 'John Doe'}]

    response = client.get('/data')
    assert response.status_code == 200
    assert response.json == [{'id': 1, 'name': 'John Doe'}]
