from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
import uvicorn
from sqlmodel import SQLModel
from contextlib import asynccontextmanager
from routers import cars, web
from routers.cars import BadtripException
from db import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(title="Car sharing", lifespan=lifespan)
app.include_router(cars.router)
app.include_router(web.router)

@app.exception_handler(BadtripException)
async def unicorn_operation_handler(request: Request, exc: BadtripException):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": "Bad Trip"},
    )

if __name__ == "main":
    uvicorn.run("carsharing:app", reload=True)