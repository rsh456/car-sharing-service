from fastapi import FastAPI
import uvicorn
from sqlmodel import SQLModel
from contextlib import asynccontextmanager
from routers import cars, web
from db import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(title="Car sharing", lifespan=lifespan)
app.include_router(cars.router)
app.include_router(web.router)

if __name__ == "main":
    uvicorn.run("carsharing:app", reload=True)