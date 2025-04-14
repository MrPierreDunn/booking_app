from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class TableBase(BaseModel):
    id: int
    name: str
    seats: int
    location: str


class TableCreate(BaseModel):
    name: str
    seats: int = Field(..., gt=0, le=10)
    location: str


class TableDelete(TableBase):
    id: int


class TableRead(TableBase):
    model_config = ConfigDict(
        from_attributes=True
    )
