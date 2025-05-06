'''
This module contains the routes for the cars API.
It includes endpoints for getting, adding, updating, and deleting cars and trips.
'''
from typing import Annotated, Union
from fastapi import HTTPException, Depends, APIRouter
from sqlmodel import Session, select
from routers.auth import get_current_user
from schemas import CarInput, CarOutput, Trip, TripInput, TripOutput, Car, User
from db import get_session

# Routers are useful for grouping related endpoints together, making it easier to maintain and understand the codebase.
router = APIRouter(prefix="/api/cars")


@router.get("/")
# Python3.5 now supports type hints
# Python 3.9+ supports annotated, a type hint that allows you to add metadata to a type
def get_cars(session: Annotated[Session, Depends(get_session)],
             size: Union[str, None] = None, doors:Union[int, None] = None)-> list:
    '''
    This function uses SQLModel - select function to get the cars from the database.
    '''
    query = select(Car)
    if size:
        query = query.where(Car.size == size)
    if doors:
        query = query.where(Car.doors >=doors)
    return session.exec(query).all()

@router.get("/{id}")
def car_by_id(session: Annotated[Session, Depends(get_session)], id: int)->CarOutput :
    car = session.get(Car, id)
    if car:
        return car
    raise HTTPException(status_code=404, detail=f"Car not found with id ={id}")

@router.post("/")
def add_car(session: Annotated[Session, Depends(get_session)],
            user: Annotated[User, Depends(get_current_user)],
            car_input: CarInput)-> Car:
    '''
    This function adds a new car to the database.
    '''
    new_car = Car.model_validate(car_input)
    session.add(new_car)
    session.commit()
    session.refresh(new_car) # Updates the car object with the new id
    return new_car
        

@router.delete("/{id}", status_code= 204)
def remove_car(session: Annotated[Session, Depends(get_session)],id: int)->None:
    '''
    This function removes a car from the database.
    '''
    car = session.get(Car, id)
    if car:
        session.delete(car)
        session.commit()
    raise HTTPException(status_code=404, detail= f"Car not found with id ={id}")
    
@router.put("/{id}")
def change_car(session: Annotated[Session, Depends(get_session)],
               id: int, new_data: CarInput) -> CarOutput:
    '''
    This function updates a car in the database, by using HTTP put method.
    '''
    car = session.get(Car, id)
    if car:
        car.size = new_data.size
        car.doors = new_data.doors
        car.fuel = new_data.fuel
        car.transmission = new_data.transmission
        session.commit()
    raise HTTPException(status_code=404, detail= f"No car with id {id} found")

class BadtripException(Exception):
    pass


@router.post("/{car_id}/trips")
def add_trip(session: Annotated[Session, Depends(get_session)],
             car_id: int, trip_input: TripInput) -> TripOutput:
    '''
    This function adds a new trip to the car.
    It uses the TripInput schema to validate the input data.
    It also checks if the trip start time is before the end time.
    '''

    car = session.get(Car, car_id)
    if car:
        new_trip = Trip.model_validate(trip_input, update={"car_id": car_id})
        if new_trip < new_trip.start:
            raise BadtripException("Trip start time must be before end time")
        car.trips.append(new_trip)
        session.commit()
        session.refresh(new_trip)
        return new_trip
    raise HTTPException(status_code=404, detail= f"No car with id {car_id} found")
