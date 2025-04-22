from fastapi import FastAPI, HTTPException
import uvicorn

app = FastAPI()
db = [
     {"id": 1, "size": "s", "fuel": "gasoline", "doors": 3, "transmission": "auto"},
     {"id": 2, "size": "s", "fuel": "electric", "doors": 3, "transmission": "auto"},
     {"id": 3, "size": "s", "fuel": "gasoline", "doors": 5, "transmission": "manual"},
     {"id": 4, "size": "m", "fuel": "electric", "doors": 3, "transmission": "auto"},
     {"id": 5, "size": "m", "fuel": "hybrid", "doors": 5, "transmission": "auto"},
     {"id": 6, "size": "m", "fuel": "gasoline", "doors": 5, "transmission": "manual"},
     {"id": 7, "size": "l", "fuel": "diesel", "doors": 5, "transmission": "manual"},
     {"id": 8, "size": "l", "fuel": "electric", "doors": 5, "transmission": "auto"},
     {"id": 9, "size": "l", "fuel": "hybrid", "doors": 5, "transmission": "auto"}
]

@app.get("/")
async def welcome(name):
    return {"message": "Welcome, {name} to the Car Sharing service!"}

@app.get("/api/cars")
# Python3.5 now supports type hints
def get_cars(size:str|None = None, doors:int|None = None)-> list:
    result = db
    if size:
        result =  [car for car in db if car['size'] == size]
    if doors:
        result =  [car for car in db if car['doors'] >= doors]
    return result

@app.get("/api/cars/{id}")
def car_by_id(id:int)->dict:
    result = [car for car in db if car['id']== id]
    if result:
        return result[0]
    else:
        raise HTTPException(status_code=404, detail="Car not found")


if __name__ == "main":
    uvicorn.run("carsharing:app", reload=True)