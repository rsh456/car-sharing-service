from fastapi import FastAPI, HTTPException, Depends
import uvicorn
from schemas import CarInput, CarOutput, Trip, TripInput, TripOutput, Car
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session, select
from contextlib import asynccontextmanager
from typing import Annotated

engine = create_engine("sqlite:///carsharing.db",
        connect_args={"check_same_thread":False}, # Needed for SQLite to work with multiple threads
        echo=True,) # Remove this in production

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(title="Car sharing", lifespan=lifespan)

## Define a method to return the session
def get_session():
    with Session(engine) as session:
        yield session


@app.get("/")
async def welcome(name):
    return {"message": "Welcome, {name} to the Car Sharing service!"}

@app.get("/api/cars")
# Python3.5 now supports type hints
# Python 3.9+ supports annotated, a type hint that allows you to add metadata to a type
def get_cars(session: Annotated[Session, Depends(get_session)],
             size:str|None = None, doors:int|None = None)-> list:
        query = select(Car)
        if size:
            query = query.where(Car.size == size)
        if doors:
            query = query.where(Car.doors >=doors)
        return session.exec(query).all()

@app.get("/api/cars/{id}")
def car_by_id(session: Annotated[Session, Depends(get_session)], id: int)->CarOutput :
    car = session.get(Car, id)
    if car:
        return car
    else:
        raise HTTPException(status_code=404, detail=f"Car not found with id ={id}")

@app.post("/api/cars")
def add_car(session: Annotated[Session, Depends(get_session)],
            car_input: CarInput)-> Car:
        new_car = Car.model_validate(car_input)
        session.add(new_car)
        session.commit()
        session.refresh(new_car) # Updates the car object with the new id
        return new_car
        

@app.delete("/api/cars/{id}", status_code= 204)
def remove_car(session: Annotated[Session, Depends(get_session)],id: int)->None:
    car = session.get(Car, id)
    if car:
        session.delete(car)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail= f"Car not found with id ={id}")
    
@app.put("/api/cars/{id}")
def change_car(session: Annotated[Session, Depends(get_session)],
               id: int, new_data: CarInput) -> CarOutput:
    car = session.get(Car, id)
    if car:
        car.size = new_data.size
        car.doors = new_data.doors
        car.fuel = new_data.fuel
        car.transmission = new_data.transmission
        session.commit()
    else:
        raise HTTPException(status_code=404, detail= f"No car with id {id} found")


@app.post("/api/cars/{car_id}/trips")
def add_trip(session: Annotated[Session, Depends(get_session)],
             car_id: int, trip_input: TripInput) -> TripOutput:
    car = session.get(Car, car_id)
    if car:
        new_trip = Trip.model_validate(trip_input, update={"car_id": car_id})
        car.trips.append(new_trip)
        session.commit()
        session.refresh(new_trip)
        return new_trip
    else:
        raise HTTPException(status_code=404, detail= f"No car with id {car_id} found")

if __name__ == "main":
    uvicorn.run("carsharing:app", reload=True)