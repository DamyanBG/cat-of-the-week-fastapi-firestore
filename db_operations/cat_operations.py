from google.cloud.exceptions import NotFound

from db import db
from models.cat_model import CatCreate, NextRoundCatModel, CurrentRoundCatModel

next_round_cat_ref = db.collection("NextRoundCats")
current_round_cat_ref = db.collection("CurrentRoundCats")


async def create_next_round_cat(cat_data: CatCreate, user_id: str) -> NextRoundCatModel:
    cat_data_dict = cat_data.model_dump()
    cat_data_dict["user_id"] = user_id
    new_cat_ref = next_round_cat_ref.document()
    await new_cat_ref.set(cat_data_dict)
    cat_data_dict["id"] = new_cat_ref.id
    next_round_cat = NextRoundCatModel(**cat_data_dict)
    return next_round_cat


async def select_not_voted_cat(voted_cats_ids: list[str]) -> CurrentRoundCatModel:
    all_cats_docs = [doc async for doc in current_round_cat_ref.stream()]
    all_cats = [
        CurrentRoundCatModel(id=cat_doc.id, **cat_doc.to_dict())
        for cat_doc in all_cats_docs
    ]
    filtered_cats = [cat for cat in all_cats if cat.id not in voted_cats_ids]

    if not filtered_cats:
        raise NotFound("No cat for vote")

    sorted_cats = sorted(filtered_cats, key=lambda cat: cat.votes)
    cat_for_vote = sorted_cats[0]

    return cat_for_vote
