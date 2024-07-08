from fastapi import APIRouter, Depends
from google.cloud.firestore import FieldFilter

from db_operations.cat_operations import create_next_round_cat
from models.cat_model import CatCreate, NextRoundCatModel, CurrentRoundCatWithPhotoUrl
from auth.token import get_current_user, TokenData


cats_router = APIRouter(prefix="/cats", tags=["cats"])



@cats_router.post("/create", response_model=NextRoundCatModel)
async def post_cat(cat: CatCreate, token_data: TokenData = Depends(get_current_user)):
    next_round_cat = await create_next_round_cat(cat, token_data.id)
    return next_round_cat


@cats_router.get("/cat-for-vote", response_model=CurrentRoundCatWithPhotoUrl)
async def get_cat_for_vote(token_data: TokenData = Depends(get_current_user)):
    user_id = token_data.id
    print("user_id")
    print(user_id)
    filter_by_user_id = FieldFilter("user_id", "==", user_id)
    user_votes_history_docs = vote_history_ref.where(filter=filter_by_user_id).stream()
    user_votes_history_cats_ids = {
        doc.to_dict()["cat_pk"] for doc in user_votes_history_docs
    }
    print("user_votes_history_cats_ids")
    print(user_votes_history_cats_ids)
    if user_votes_history_cats_ids:
        current_round_cats_query = current_round_cat_ref.where(
            "id", "not-in", list(user_votes_history_cats_ids)
        )
        current_round_cats_docs = (
            current_round_cats_query.order_by("votes").limit(1).stream()
        )
    else:
        current_round_cats_docs = (
            current_round_cat_ref.order_by("votes").limit(1).stream()
        )

    print("current_round_cats_docs")
    print(current_round_cats_docs)
    cat_for_vote_doc = next(current_round_cats_docs, None)
    cat_for_vote = cat_for_vote_doc.to_dict()
    cat_for_vote["id"] = cat_for_vote_doc.id
    cat_image_filter = FieldFilter("__name__", "==", cat_for_vote["photo_id"])
    print("the photo id")
    print(cat_for_vote["photo_id"])
    photo_docs = image_ref.document(cat_for_vote["photo_id"]).get()
    print("photo_docs")
    print(photo_docs.to_dict())
    for doc in photo_docs:
        print("doc")
        print(doc)
    photo_doc = next(photo_docs, None)
    photo_data = photo_doc.to_dict()
    print(photo_doc)
    cat_for_vote["photo_url"] = photo_data["image_url"]
    print(cat_for_vote)

    return cat_for_vote
