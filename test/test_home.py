'''
This test uses FastAPI's TestClient to simulate requests to the API templates and check the responses.
'''
from fastapi.testclient import TestClient

from carsharing import app

client = TestClient(app)


def test_home():
    '''
    Test the home page of the web application.
    '''
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome" in response.text