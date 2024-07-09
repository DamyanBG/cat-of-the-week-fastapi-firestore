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
    photo_id: Optional[str]


class CatCreate(BaseCatModel):
    pass


class CurrentRoundCatModel(BaseCatModel):
    id: str
    user_id: Optional[str]
    likes: int = 0
    dislikes: int = 0
    votes: int = 0


class CurrentRoundCatWithPhotoUrl(BaseCatModel):
    id: str
    user_id: Optional[str]
    likes: int = 0
    dislikes: int = 0
    votes: int = 0
    photo_url: str


class NextRoundCatModel(BaseCatModel):
    id: str
    user_id: Optional[str]


class CatOfTheWeekBase(BaseCatModel):
    user_id: str
    week_number: int
    year: int
    likes: int
    dislikes: int
    votes: int


class CatOfTheWeekModel(CatOfTheWeekBase):
    id: str


class CatOfTheWeekWithImage(CatOfTheWeekModel):
    image_url: str


class CatOfTheWeekCreate(CatOfTheWeekBase):
    pass
