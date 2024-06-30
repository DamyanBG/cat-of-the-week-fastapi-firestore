from db import db
from models.cat_model import NextRoundCatModel

next_rc_ref = db.collection("NextRoundCats")
current_rc_ref = db.collection("CurrentRoundCats")


def win_job():
    print("win_job")
    next_round_cats_docs = next_rc_ref.stream()
    for cat_doc in next_round_cats_docs:
        print(cat_doc.id)
        cat_data = cat_doc.to_dict()
        # TO FINISH THE LOGIC
        next_round_cat = NextRoundCatModel(**cat_data)
        print(cat_data)
        new_current_rc_doc_ref = current_rc_ref.document()
        new_current_rc_doc_ref.set(cat_data)
        print("ok")
        cat_doc.reference.delete()
