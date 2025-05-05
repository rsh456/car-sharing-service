from fastapi.testclient import TestClient
from carsharing import app

from routers.cars import add_car
from schemas import CarInput, User, Car
from unittest.mock import Mock

client = TestClient(app)

def test_add_car():
    response = client.post("/api/cars/", json={"doors": 4,"size": "compact"}, 
                           headers={'Authorization': 'Bearer admin'}
                           )
    assert response.status_code == 200
    car = response.json()
    assert car["doors"] == 4
    assert car["size"] == "compact"


def test_add_car_with_mock_session():
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
