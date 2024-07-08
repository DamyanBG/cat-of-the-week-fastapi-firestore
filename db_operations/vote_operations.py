from google.cloud.firestore import FieldFilter

from db import db


vote_history_ref = db.collection("VoteHistory")


async def select_user_voted_cats_ids(user_id: str) -> list[str]:
    filter_by_user_id = FieldFilter("user_id", "==", user_id)
    query = vote_history_ref.where(filter=filter_by_user_id)
    user_voted_cats_ids = [doc["id"] async for doc in query.stream()]
    return user_voted_cats_ids
