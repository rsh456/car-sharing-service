import json
from pydantic import BaseModel
# By creating a class that inherits from BaseModel and listing fields, we get a dunder init method
from sqlmodel import Relationship, SQLModel, Field, Relationship, Column, VARCHAR
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])

# This class adds security preventing password leaking
class UserOutput(SQLModel):
    id: int
    username: str

class User(SQLModel, table = True):
    id: int | None= Field(default=None, primary_key=True)
    
    # Add a constrait to prevent duplicate usernames 
    # and a unique index to speed up queries
    username: str = Field(sa_column=Column("username", VARCHAR, unique=True, index=True))
    password_hash: str =""

    def set_password(self, password: str):
        self.password_hash = password

    def verify_password(self, password: str):
        return pwd_context.verify(password, self.password_hash)


class TripInput(SQLModel):
    start:int
    end: int
    description:str

class TripOutput(TripInput):
    id: int

class Trip(TripInput, table=True):
    id: int |None = Field(default=None, primary_key=True)
    car_id : int = Field(foreign_key="car.id")

    car: "Car" = Relationship(back_populates="trips") # Car is not implemented yet, so we use a string to avoid circular import issues

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