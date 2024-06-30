from pydantic import BaseModel, Field


class VoteHistory(BaseModel):
    id: str = Field(...)
    user_id: str = Field(...)
    cat_id: str = Field(...)
