from pydantic import BaseModel, Field
from datetime import datetime

from typing import Optional


class BaseCatModel(BaseModel):
    name: str
    created_on: Optional[datetime] = Field(default_factory=datetime.now)
    birth_date: Optional[datetime]
    microchip: Optional[str]
    color: Optional[str]
    breed: Optional[str]
    photo_id: Optional[int]

    class Config:
        orm_mode = True


class CatCreate(BaseCatModel):
    pass


class CurrentRoundCatSchema(BaseCatModel):
    id: str
    user_id: Optional[int]
    likes: int = 0
    dislikes: int = 0
    votes: int = 0


class NextRoundCatSchema(BaseCatModel):
    id: str
    user_id: Optional[int]



class CatOfTheWeekSchema(BaseCatModel):
    id: str
    user_id: Optional[int]
    the_week: Optional[datetime]
