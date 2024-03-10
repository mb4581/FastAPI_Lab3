from fastapi import FastAPI

from public.films import films_router
from public.producers import producers_router

app = FastAPI()

app.include_router(producers_router)
app.include_router(films_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
