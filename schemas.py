'''
This module contains the schemas for the API.
It defines the data models used for user authentication, car information, and trip details.
'''
import json
from typing import Union
# By creating a class that inherits from BaseModel and listing fields, we get a dunder init method
from sqlmodel import Relationship, SQLModel, Field, Relationship, Column, VARCHAR
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])

class UserOutput(SQLModel):
    '''
    This class is used to output the user information.
    This class adds security preventing password leaking
    '''
    id: int
    username: str

class User(SQLModel, table = True):
    id:Union[int, None] = Field(default=None, primary_key=True)
    '''
    Add a constrait to prevent duplicate usernames and a unique index to speed up queries
    '''
    username: str = Field(sa_column=Column("username", VARCHAR, unique=True, index=True))
    password_hash: str =""

    def set_password(self, password: str):
        '''
        This function is used to set the password for the user.
        It uses the passlib library to hash the password.
        '''
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password: str):
        '''
        This function is used to verify the password for the user.
        It uses the passlib library to verify the password.
        '''
        return pwd_context.verify(password, self.password_hash)


class TripInput(SQLModel):
    '''
    This class is used to input the trip information.
    '''
    start:int
    end: int
    description:str

class TripOutput(TripInput):
    '''
    This class is used to output the trip information.
    '''
    id: int

class Trip(TripInput, table=True):
    '''
    This class is used to store the trip information.
    It inherits from TripInput and adds the id and car_id fields.
    '''
    id: int |None = Field(default=None, primary_key=True)
    car_id : int = Field(foreign_key="car.id")
    # Car is not implemented yet used a string to avoid circular import issues
    car: "Car" = Relationship(back_populates="trips") 

class CarInput(SQLModel):
    '''
    This class is used to input the car information.
    '''
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
    '''
    This class is used to store the car information.
    It inherits from CarInput and adds the id field.
    '''
    id: int | None = Field(primary_key=True, default=None)
    trips: list[Trip] = Relationship(back_populates="car")

class CarOutput(CarInput):
    '''
    This class is used to output the car information.
    '''
    id: int
    trips: list[TripInput] = []
