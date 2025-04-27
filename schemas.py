import json
from pydantic import BaseModel
# By creating a class that inherits from BaseModel and listing fields, we get a dunder init method
from sqlmodel import Relationship, SQLModel, Field


class TripInput(SQLModel):
    start:int
    end: int
    description:str

class TripOutput(TripInput):
    id: int

class Trip(TripInput, table=True):
    id: int |None = Field(default=None, primary_key=True)
    car_id : int = Field(foreign_key="car.id")

    car: "Car" = Relationship(back_populates="trips")

class CarInput(SQLModel):
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

class Car(CarInput, table=True):
    id: int | None = Field(primary_key=True, default=None)
    trips: list[Trip] = Relationship(back_populates="car")

class CarOutput(CarInput):
    id: int
    trips: list[TripInput] = []