from fastapi import APIRouter
from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound

from db import make_session
from models.common import ErrorModel, SuccessModel
from models.films import FilmModel, FilmCreationModel, FilmPatchModel
from orm.entities import Film

films_router = APIRouter(tags=['Films'], prefix='/api/films')


@films_router.get('/')
async def list_all_films() -> list[FilmModel]:
    """
    Получить список всех известных системе фильмов
    """
    async with make_session() as session:
        query = await session.execute(select(Film).order_by(Film.id))
        out = []
        for film, in query:
            out.append(film)
    return out


@films_router.get('/{film_id}')
async def get_film(film_id: int) -> FilmModel | ErrorModel:
    """
    Получить информацию об одном конкретном фильме
    """
    async with make_session() as session:
        query = select(Film).where(Film.id == film_id)
        selection = await session.execute(query)
        try:
            return selection.scalar_one()
        except NoResultFound:
            return ErrorModel(error="Film doesn't exist")


@films_router.put('/{film_id}')
async def override_film(film_id: int, film_body: FilmCreationModel) -> FilmModel | ErrorModel:
    """
    Заменить информацию об одном конкретном фильме
    """
    async with make_session() as session:
        query = update(Film).where(Film.id == film_id)\
            .values(**film_body.model_dump())
        await session.execute(query)
        await session.commit()
    return await get_film(film_id)


@films_router.patch('/{film_id}')
async def patch_film(film_id: int, film_body: FilmPatchModel) -> FilmModel | ErrorModel:
    """
    Заменить часть информации об одном конкретном фильме
    """
    async with make_session() as session:
        query = update(Film).where(Film.id == film_id)\
            .values(**film_body.get_values())
        await session.execute(query)
        await session.commit()
    return await get_film(film_id)


@films_router.post('/')
async def create_film(film_model: FilmCreationModel) -> FilmModel | ErrorModel:
    """
    Добавить новый фильм
    """
    async with make_session() as session:
        film = Film(**film_model.model_dump())
        session.add(film)
        await session.commit()
    return await get_film(film.id)


@films_router.delete('/{film_id}')
async def delete_film(film_id: int) -> SuccessModel | ErrorModel:
    """
    Удаляет фильм
    """
    async with make_session() as session:
        query = select(Film).where(Film.id == film_id)
        selection = await session.execute(query)
        try:
            entry = selection.scalar_one()              # type: Film
            await session.delete(entry)
            await session.commit()
            return SuccessModel(success=True)
        except NoResultFound:
            return ErrorModel(error="Film doesn't exist")
