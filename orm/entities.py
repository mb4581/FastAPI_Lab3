from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Producer(Base):
    """
    Сущность "Пользователь"
    """
    __tablename__ = 'producers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)


class Film(Base):
    """
    Сущность "Фильм"
    """
    __tablename__ = 'films'
    id = Column(Integer, primary_key=True, autoincrement=True)
    producer_id = Column(Integer, ForeignKey("producers.id"), nullable=False)

    title = Column(String, nullable=False)
    summary = Column(String, default="")
    year = Column(Integer, nullable=False)

    producer = relationship("Producer",
                            foreign_keys="Film.producer_id",
                            lazy="joined")
