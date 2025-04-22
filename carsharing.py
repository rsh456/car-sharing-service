from fastapi import FastAPI, HTTPException
import uvicorn
from schemas import load_db

app = FastAPI()
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
def car_by_id(id:int):
    result = [car for car in db if car.id== id]
    if result:
        return result[0]
    else:
        raise HTTPException(status_code=404, detail="Car not found")


if __name__ == "main":
    uvicorn.run("carsharing:app", reload=True)