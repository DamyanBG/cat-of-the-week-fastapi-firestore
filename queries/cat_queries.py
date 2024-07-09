from typing import Optional
from google.cloud.exceptions import NotFound
from google.cloud.firestore import FieldFilter, Increment
from datetime import date

from db import db
from models.cat_model import (
    CatCreate,
    NextRoundCatModel,
    CurrentRoundCatModel,
    CatOfTheWeekModel,
)

next_round_cat_ref = db.collection("NextRoundCats")
current_round_cat_ref = db.collection("CurrentRoundCats")
cat_of_the_week_ref = db.collection("CatsOfTheWeeks")


def get_current_week_and_year():
    today = date.today()
    year, week_number, _ = today.isocalendar()
    return week_number, year


async def select_cat_of_the_week() -> Optional[CatOfTheWeekModel]:
    week_number, year = get_current_week_and_year()

    filter_week = FieldFilter("week_number", "==", week_number)
    filter_year = FieldFilter("year", "==", year)
    query = cat_of_the_week_ref.where(filter=filter_week).where(filter=filter_year)

    docs = [doc async for doc in query.stream()]
    if not docs:
        return None

    cat_doc = docs[0]
    cat = CatOfTheWeekModel(id=cat_doc.id, **cat_doc.to_dict())
    return cat


async def select_cat_by_user_id(user_id: str) -> Optional[NextRoundCatModel]:
    filter_field = FieldFilter("user_id", "==", user_id)
    query = next_round_cat_ref.where(filter=filter_field)
    docs = [doc async for doc in query.stream()]
    if not docs:
        return None

    cat_doc = docs[0]
    cat = NextRoundCatModel(id=cat_doc.id, **cat_doc.to_dict())
    return cat


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


async def add_like(cat_id: str) -> None:
    cat_doc_ref = current_round_cat_ref.document(cat_id)
    await cat_doc_ref.update({"likes": Increment(1), "votes": Increment(1)})


async def add_dislike(cat_id: str) -> None:
    cat_doc_ref = current_round_cat_ref.document(cat_id)
    await cat_doc_ref.update({"dislikes": Increment(1), "votes": Increment(1)})
