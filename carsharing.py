from fastapi import FastAPI, HTTPException
import uvicorn
from schemas import load_db, CarInput, CarOutput, save_db, TripInput, TripOutput

app = FastAPI(title="Car sharing")
db = load_db()

@app.get("/")
async def welcome(name):
    return {"message": "Welcome, {name} to the Car Sharing service!"}

@app.get("/api/cars")
# Python3.5 now supports type hints
def get_cars(size:str|None = None, doors:int|None = None)-> list:
    result = db
    if size:
        result =  [car for car in db if car.size == size]
    if doors:
        result =  [car for car in db if car.doors >= doors]
    return result

@app.get("/api/cars/{id}")
def car_by_id(id: int) :
    result = [car for car in db if car.id== id]
    if result:
        return result[0]
    else:
        raise HTTPException(status_code=404, detail=f"Car not found with id ={id}")

@app.post("/api/cars")
def add_car(car: CarInput)-> CarOutput:
    new_car = CarOutput(size=car.size, doors=car.doors, fuel=car.fuel, 
                        transmission=car.transmission, id=len(db)+1)
    db.append(new_car)
    save_db(db)
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