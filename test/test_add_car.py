'''
Test the add_car function in the cars router.
This test uses FastAPI's TestClient to simulate requests to the API and check the responses.
'''
from fastapi.testclient import TestClient
from carsharing import app

from routers.cars import add_car
from schemas import CarInput, User, Car
from unittest.mock import Mock

client = TestClient(app)

def test_add_car():
    '''
    Test the add_car function in the cars router.
    '''
    response = client.post("/api/cars/", json={"doors": 4,"size": "compact"}, 
                           headers={'Authorization': 'Bearer admin'}
                           )
    assert response.status_code == 200
    car = response.json()
    assert car["doors"] == 4
    assert car["size"] == "compact"


def test_add_car_with_mock_session():
    '''
    Test the add_car function using a mock session.
    This test does not require a real database connection.
    '''
    mock_session= Mock()
    input_data = CarInput(doors=4, size="compact")
    user = User(username="test_user")
    result = add_car(car_input=input_data, session=mock_session, user=user)

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()

    assert isinstance(result, Car)
    assert result.doors == 4
    assert result.size == "compact"
