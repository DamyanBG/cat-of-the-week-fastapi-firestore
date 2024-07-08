from google.cloud.firestore import FieldFilter
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
    if voted_cats_ids:
        field_filter = FieldFilter("id", "not-in", list(voted_cats_ids))
        query = (
            current_round_cat_ref.where(filter=field_filter).order_by("votes").limit(1)
        )
    else:
        query = current_round_cat_ref.order_by("votes").limit(1)

    docs = [doc async for doc in query.stream()]
    if not docs:
        raise NotFound("No cat for vote")

    not_voted_cat_doc = docs[0]
    not_voted_cat_dict = not_voted_cat_doc.to_dict()
    not_voted_cat_dict["id"] = not_voted_cat_doc.id

    not_voted_cat = CurrentRoundCatModel(**not_voted_cat_dict)
    return not_voted_cat
