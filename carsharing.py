from contextlib import asynccontextmanager
from db import engine
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from sqlmodel import SQLModel
from routers import cars, web, auth
from routers.cars import BadtripException


@asynccontextmanager
async def lifespan(app: FastAPI):
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
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": "Bad Trip"},
    )

@app.middleware("http")
async def add_cars_cookie(request:Request, call_next):
    response = await call_next(request)
    response.set_cookie(key="cars_cookie", value="you visitedc the carsharing app")
    return response

if __name__ == "main":
    uvicorn.run("carsharing:app", reload=True)
