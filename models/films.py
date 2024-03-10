from typing import Optional

from pydantic import BaseModel, Field

from models.producer import ProducerModel


class FilmCreationModel(BaseModel):
    producer_id: int
    title: str
    summary: Optional[str] = Field("")
    year: int


class FilmModel(BaseModel):
    id: int
    producer: ProducerModel
    title: str
    summary: Optional[str] = Field("")
    year: int


class FilmPatchModel(BaseModel):
    producer_id: Optional[int] = Field(None)
    title: Optional[str] = Field(None)
    summary: Optional[str] = Field(None)
    year: Optional[int] = Field(None)

    def get_values(self):
        return dict((k, v) for k, v in self.model_dump().items() if v is not None)
