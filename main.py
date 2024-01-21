from fastapi import FastAPI

from db import create_tables_at_start
from public.films import films_router
from public.producers import producers_router

app = FastAPI(lifespan=create_tables_at_start)

app.include_router(producers_router)
app.include_router(films_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
