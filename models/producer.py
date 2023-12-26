from typing import Optional

from pydantic import BaseModel, Field


class ProducerCreateModel(BaseModel):
    first_name: str
    last_name: str


class ProducerModel(ProducerCreateModel):
    id: int


class ProducerPatchModel(BaseModel):
    first_name: Optional[str] = Field(None)
    last_name: Optional[str] = Field(None)

    def get_values(self):
        return dict((k, v) for k, v in self.model_dump().items() if v is not None)
