'''
This is the main file for the carsharing application.
It initializes the FastAPI application, sets up the database connection, and includes the routers for different functionalities.
'''
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from sqlmodel import SQLModel
from routers import cars, web, auth
from routers.cars import BadtripException
from db import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    '''
    This function sets up the lifespan of the FastAPI application.
    It creates the database tables when the application starts and drops them when it stops.
    '''
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(title="Car sharing", lifespan=lifespan)
app.include_router(cars.router)
app.include_router(web.router)
app.include_router(auth.router)

origins = [
    "http://localhost:8000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(BadtripException)
async def unicorn_operation_handler(request: Request, exc: BadtripException):
    '''
    This function handles the BadtripException.
    It returns a JSON response with a 422 status code and a message indicating a bad trip.
    '''
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": "Bad Trip"},
    )

@app.middleware("http")
async def add_cars_cookie(request:Request, call_next):
    '''
    This middleware sets a cookie for the carsharing application.
    '''
    response = await call_next(request)
    response.set_cookie(key="cars_cookie", value="you visitedc the carsharing app")
    return response

if __name__ == "main":
    '''
    This is the entry point of the application.
    It runs the FastAPI application using Uvicorn.
    '''
    uvicorn.run("carsharing:app", reload=True)
