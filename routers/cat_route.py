from fastapi import APIRouter, Depends, HTTPException
from google.cloud.exceptions import NotFound

from db_operations.cat_operations import create_next_round_cat, select_not_voted_cat
from db_operations.vote_operations import select_user_voted_cats_ids
from db_operations.image_operations import select_image_file_name_by_id
from models.cat_model import CatCreate, NextRoundCatModel, CurrentRoundCatWithPhotoUrl
from models.user_model import UserId
from auth.token import get_current_user
from storage.google_cloud_storage import generate_signed_url


cats_router = APIRouter(prefix="/cats", tags=["cats"])


@cats_router.post("/create", response_model=NextRoundCatModel)
async def post_cat(cat: CatCreate, user_id: UserId = Depends(get_current_user)):
    next_round_cat = await create_next_round_cat(cat, user_id.id)
    return next_round_cat


@cats_router.get("/cat-for-vote", response_model=CurrentRoundCatWithPhotoUrl)
async def get_cat_for_vote(user_id: UserId = Depends(get_current_user)):
    user_id = user_id.id
    user_votes_history_cats_ids = await select_user_voted_cats_ids(user_id)
    try:
        cat_for_vote = await select_not_voted_cat(user_votes_history_cats_ids)
    except NotFound:
        raise HTTPException(status_code=404, detail="Cat not found!")
    cat_image_file_name = await select_image_file_name_by_id(cat_for_vote.photo_id)
    cat_image_url = generate_signed_url(cat_image_file_name)
    cat_for_vote_with_image = CurrentRoundCatWithPhotoUrl(
        **{"photo_url": cat_image_url}, **cat_for_vote.model_dump()
    )
    cat_for_vote_with_image

    return cat_for_vote_with_image
