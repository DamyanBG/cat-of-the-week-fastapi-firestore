from typing import Union
from fastapi import APIRouter, Depends, HTTPException, status
from google.cloud.exceptions import NotFound

from queries.cat_queries import (
    create_next_round_cat,
    select_not_voted_cat,
    select_cat_by_user_id,
    select_cat_of_the_week,
)
from queries.vote_queries import select_user_voted_cats_ids
from queries.image_queries import select_image_file_name_by_id
from models.cat_model import (
    CatCreate,
    NextRoundCatModel,
    CurrentRoundCatWithPhotoUrl,
    CatOfTheWeekWithImage,
    NextRoundCatWithImage,
)
from models.user_model import UserId
from auth.token import get_current_user
from storage.google_cloud_storage import generate_signed_url


cats_router = APIRouter(prefix="/cats", tags=["cats"])


@cats_router.post(
    "/create", response_model=NextRoundCatModel, status_code=status.HTTP_201_CREATED
)
async def post_cat(cat: CatCreate, user_id: UserId = Depends(get_current_user)):
    existing_cat = await select_cat_by_user_id(user_id.id)
    if existing_cat:
        raise HTTPException(status_code=400, detail="You already uploaded a cat!")

    next_round_cat = await create_next_round_cat(cat, user_id.id)
    return next_round_cat


@cats_router.get("/cat-for-vote", response_model=Union[CurrentRoundCatWithPhotoUrl, dict[str, str]])
async def get_cat_for_vote(user_id: UserId = Depends(get_current_user)):
    user_id = user_id.id
    user_votes_history_cats_ids = await select_user_voted_cats_ids(user_id)
    try:
        cat_for_vote = await select_not_voted_cat(user_votes_history_cats_ids)
    except NotFound:
        return {"message": "No cat for vote!"}
    cat_image_file_name = await select_image_file_name_by_id(cat_for_vote.photo_id)
    cat_image_url = generate_signed_url(cat_image_file_name)
    cat_for_vote_with_image = CurrentRoundCatWithPhotoUrl(
        **{"photo_url": cat_image_url}, **cat_for_vote.model_dump()
    )
    cat_for_vote_with_image

    return cat_for_vote_with_image


@cats_router.get("/cat-of-the-week", response_model=CatOfTheWeekWithImage)
async def get_cat_of_the_week():
    cat_of_the_week = await select_cat_of_the_week()
    cat_image_file_name = await select_image_file_name_by_id(cat_of_the_week.photo_id)
    cat_image_url = generate_signed_url(cat_image_file_name)
    cat_with_image = CatOfTheWeekWithImage(
        image_url=cat_image_url, **cat_of_the_week.model_dump()
    )
    return cat_with_image


@cats_router.get("/user-cat", response_model=NextRoundCatWithImage)
async def get_user_cat(user_id: UserId = Depends(get_current_user)):
    user_cat = await select_cat_by_user_id(user_id.id)
    cat_image_file_name = await select_image_file_name_by_id(user_cat.photo_id)
    cat_image_url = generate_signed_url(cat_image_file_name)
    user_cat_with_image = NextRoundCatWithImage(
        image_url=cat_image_url, **user_cat.model_dump()
    )

    return user_cat_with_image
