'''
It tests the `/api/cars` endpoint to ensure that it returns a list of cars with the expected attributes.
'''
from fastapi.testclient import TestClient
from carsharing import app

client = TestClient(app)

def test_get_cars():
    '''
    Test the get_cars function in the cars router.
    '''
    response = client.get("/api/cars")
    assert response.status_code == 200
    cars = response.json()
    assert all("doors" in c for c in cars)
    assert all("size" in c for c in cars)
