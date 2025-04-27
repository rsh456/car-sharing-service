from fastapi import FastAPI, HTTPException, Depends
import uvicorn
from schemas import load_db, CarInput, CarOutput, save_db, TripInput, TripOutput, Car
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session, select
from contextlib import asynccontextmanager
from typing import Annotated

engine = create_engine("sqlite:///carsharing.db",
        connect_args={"check_same_thread":False}, # Needed for SQLite to work with multiple threads
        echo=True,)

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(title="Car sharing", lifespan=lifespan)
db = load_db()

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
def car_by_id(id: int) :
    result = [car for car in db if car.id== id]
    if result:
        return result[0]
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
def remove_car(id: int)->None:
    matches = [car for car in db if car.id == id]
    if matches:
        car = matches[0]
        db.remove(car)
        save_db(db)
    else:
        raise HTTPException(status_code=404, detail= f"Car not found with id ={id}")

@app.put("/api/cars/{id}")
def change_car(id: int, new_data: CarInput) -> CarOutput:
    print("1")
    matches = [car for car in db if car.id == id]
    print("2")
    if matches:
       car = matches[0]
       car.fuel = new_data.fuel
       car.transmission = new_data.transmission
       car.size = new_data.size
       car.doors = new_data.doors
       save_db(db)
       return car
    else:
        raise HTTPException(status_code=404, detail= f"No car with id {id} found")


@app.post("/api/cars/{car_id}/trips")
def add_trip(car_id: int, trip: TripInput) -> TripOutput:
    matches = [car for car in db if car.id == car_id] 
    if matches:
        car = matches[0]
        new_trip = TripOutput(id = len(car.trips)+1,
                              start = trip.start, 
                              end = trip.end, 
                              description = trip.description)
        car.trips.append(new_trip)
        save_db(db)
        return new_trip
    else:
        raise HTTPException(status_code=404, detail= f"No car with id {car_id} found")

if __name__ == "main":
    uvicorn.run("carsharing:app", reload=True)