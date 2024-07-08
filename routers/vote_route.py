from fastapi import APIRouter, Depends

from models.vote_models import VoteCreate, VoteHistory, VoteHistoryCreate
from models.user_model import UserId
from db_operations.vote_operations import insert_vote_history
from auth.token import get_current_user

vote_router = APIRouter(prefix="/vote", tags=["vote"])


@vote_router.post("/", response_model=VoteHistory)
async def post_vote(vote: VoteCreate, user_id: UserId = Depends(get_current_user)):
    vote_history_data = VoteHistoryCreate(user_id=user_id.id, cat_id=vote.cat_id)
    vote_history = await insert_vote_history(vote_history_data)

    return vote_history
