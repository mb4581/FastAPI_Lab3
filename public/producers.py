from fastapi import APIRouter, Response
from sqlalchemy import select, update, delete
from sqlalchemy.exc import NoResultFound, IntegrityError

from db import make_session
from models.common import ErrorModel, SuccessModel
from models.producer import ProducerModel, ProducerCreateModel, ProducerPatchModel
from orm.entities import Producer

producers_router = APIRouter(tags=['Producers'], prefix='/api/producers')


@producers_router.get('/')
async def list_all_producers() -> list[ProducerModel]:
    """
    Получить список всех известных системе продюсеров
    """
    async with make_session() as session:
        query = await session.execute(select(Producer).order_by(Producer.id))
        out = []
        for producer, in query:
            out.append(producer)
    return out


@producers_router.get('/{producer_id}')
async def get_producer(producer_id: int, response: Response) -> ProducerModel | ErrorModel:
    """
    Получить информацию об одном конкретном продюсере
    """
    async with make_session() as session:
        query = select(Producer).where(Producer.id == producer_id)
        selection = await session.execute(query)
        try:
            return selection.scalar_one()
        except NoResultFound:
            response.status_code = 404
            return ErrorModel(error="Producer doesn't exist")


@producers_router.put('/{producer_id}')
async def override_producer(producer_id: int, producer_body: ProducerCreateModel, response: Response) -> ProducerModel | ErrorModel:
    """
    Заменить информацию об одном конкретном продюсере
    """
    async with make_session() as session:
        query = update(Producer).where(Producer.id == producer_id)\
            .values(**producer_body.model_dump())
        await session.execute(query)
        await session.commit()
    return await get_producer(producer_id, response)


@producers_router.patch('/{producer_id}')
async def patch_producer(producer_id: int, producer_body: ProducerPatchModel, response: Response) -> ProducerModel | ErrorModel:
    """
    Заменить часть информации об одном конкретном продюсере
    """
    async with make_session() as session:
        query = update(Producer).where(Producer.id == producer_id)\
            .values(**producer_body.get_values())
        await session.execute(query)
        await session.commit()
    return await get_producer(producer_id, response)


@producers_router.post('/')
async def create_producer(producer_model: ProducerCreateModel) -> ProducerModel | ErrorModel:
    """
    Добавить носового продюсера
    """
    async with make_session() as session:
        producer = Producer(**producer_model.model_dump())
        session.add(producer)
        await session.commit()
        return ProducerModel(id=producer.id,
                             first_name=producer.first_name,
                             last_name=producer.last_name)


@producers_router.delete('/{producer_id}')
async def delete_producer(producer_id: int, response: Response) -> SuccessModel | ErrorModel:
    """
    Удаляет продюсера
    """
    async with make_session() as session:
        try:
            query = delete(Producer).where(Producer.id == producer_id)
            await session.execute(query)
            await session.commit()
            return SuccessModel(success=True)
        except IntegrityError:
            response.status_code = 400
            return ErrorModel(error="Producer is used in some films and can't de deleted")
