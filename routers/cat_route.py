from fastapi import APIRouter, Depends

from db_operations.cat_operations import create_next_round_cat, select_not_voted_cat
from db_operations.vote_operations import select_user_voted_cats_ids
from db_operations.image_operations import select_image_url_by_id
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
    user_votes_history_cats_ids = await select_user_voted_cats_ids(user_id)
    cat_for_vote = await select_not_voted_cat(user_votes_history_cats_ids)
    cat_image_url = await select_image_url_by_id(cat_for_vote.photo_id)
    cat_for_vote_with_image = CurrentRoundCatWithPhotoUrl(
        **{"photo_url": cat_image_url}, **cat_for_vote.model_dump()
    )
    cat_for_vote_with_image

    return cat_for_vote_with_image
