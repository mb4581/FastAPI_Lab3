from fastapi import FastAPI

from db import create_tables
from public.films import films_router
from public.producers import producers_router

app = FastAPI()

app.include_router(producers_router)
app.include_router(films_router)


@app.on_event("startup")
async def startup_event():
    # Создание таблиц в БД
    await create_tables()


@app.get("/")
async def root():
    return {"message": "Hello World"}
