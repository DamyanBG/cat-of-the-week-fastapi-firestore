from pydantic import BaseModel, Field
from datetime import datetime

from typing import Optional


class BaseCatSchema(BaseModel):
    pk: Optional[int]
    name: str
    created_on: Optional[datetime] = Field(default_factory=datetime.now)
    birth_date: Optional[datetime]
    microchip: Optional[str]
    color: Optional[str]
    breed: Optional[str]

    class Config:
        orm_mode = True


class CurrentRoundCatSchema(BaseCatSchema):
    user_pk: Optional[int]
    likes: int = 0
    dislikes: int = 0
    votes: int = 0
    photo_pk: Optional[int]


class NextRoundCatSchema(BaseCatSchema):
    user_pk: Optional[int]
    photo_pk: Optional[int]


class CatOfTheWeekSchema(BaseCatSchema):
    user_pk: Optional[int]
    photo_pk: Optional[int]
    the_week: Optional[datetime]
