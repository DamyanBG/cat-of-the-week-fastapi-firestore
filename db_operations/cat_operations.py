from db import db
from models.cat_model import CatCreate, NextRoundCatModel

next_round_cat_ref = db.collection("NextRoundCats")
current_round_cat_ref = db.collection("CurrentRoundCats")
vote_history_ref = db.collection("VoteHistory")
image_ref = db.collection("Images")


async def create_next_round_cat(cat_data: CatCreate, user_id: str) -> NextRoundCatModel:
    cat_data_dict = cat_data.model_dump()
    cat_data["user_id"] = user_id
    new_cat_ref = next_round_cat_ref.document()
    await new_cat_ref.set(cat_data_dict)
    cat_data_dict["id"] = new_cat_ref.id
    next_round_cat = NextRoundCatModel(**cat_data_dict)
    return next_round_cat


