from google.cloud.firestore import FieldFilter

from db import db
from models.vote_models import VoteHistoryCreate, VoteHistory


vote_history_ref = db.collection("VoteHistory")


async def select_user_voted_cats_ids(user_id: str) -> list[str]:
    filter_by_user_id = FieldFilter("user_id", "==", user_id)
    query = vote_history_ref.where(filter=filter_by_user_id)
    user_voted_cats_ids = [doc.to_dict()["cat_id"] async for doc in query.stream()]
    return user_voted_cats_ids


async def insert_vote_history(vote_history_data: VoteHistoryCreate) -> VoteHistory:
    vote_history_dict = vote_history_data.model_dump()
    new_vote_history_ref = vote_history_ref.document()
    await new_vote_history_ref.set(vote_history_dict)
    vote_history_dict["id"] = new_vote_history_ref.id
    vote_history = VoteHistory(**vote_history_dict)
    return vote_history
