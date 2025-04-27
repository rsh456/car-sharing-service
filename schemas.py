import json
from pydantic import BaseModel
# By creating a class that inherits from BaseModel and listing fields, we get a dunder init method

class TripInput(BaseModel):
    start:int
    end: int
    description:str

class TripOutput(TripInput):
    id: int

class CarInput(BaseModel):
    size: str
    fuel: str | None = "electric"
    doors: int
    transmission: str | None = "auto"

    # model_config provides an example for the JSON schema
    # This is used by FastAPI to generate the OpenAPI schema and documentation
    model_config ={
        "json_schema_extra":{
            "examples":[
                {
                    "size": "m",
                    "doors": 5,
                    "transmission": "auto",
                    "fuel": "hybrid"
                }
            ]
        }
    }

class CarOutput(CarInput):
    id: int
    trips: list[TripInput] = []

def load_db()->list[CarOutput]:
    with open("cars.json", 'r') as file:
        return [CarOutput.model_validate(obj) for obj in json.load(file)]
    
def save_db(cars: list[CarOutput])->None:
    with open("cars.json", 'w') as file:
        json.dump([car.model_dump() for car in cars], file, indent=4)
