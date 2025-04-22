from pydantic import BaseModel
# By creating a class that inherits from BaseModel and listing fields, we get a dunder init method
import json


class Car(BaseModel):
    id: int
    size: str
    fuel: str | None = "electric"
    doors: int
    transmission: str | None = "auto"

def load_db()->list[Car]:
    with open("cars.json", "r") as file:
        return [Car.model_validate(obj) for obj in json.load(file)]