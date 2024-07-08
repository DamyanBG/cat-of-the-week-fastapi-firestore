from pydantic import BaseModel, Field

from utils.enums import VoteEnum


class VoteHistoryBase(BaseModel):
    user_id: str = Field(...)
    cat_id: str = Field(...)


class VoteHistoryCreate(VoteHistoryBase):
    pass


class VoteHistory(VoteHistoryBase):
    id: str = Field(...)


class VoteBase(BaseModel):
    vote: VoteEnum


class VoteCreate(VoteBase):
    cat_id: str
