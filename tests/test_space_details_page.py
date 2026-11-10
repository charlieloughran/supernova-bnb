from app import app 
from lib.database_connection import DatabaseConnection

"""
get_space_details returns status 200
"""
def test_get_space_details_returns_correctly():
    client = app.test_client()

    response = client.get("/spaces/1")

    assert response.status_code == 200