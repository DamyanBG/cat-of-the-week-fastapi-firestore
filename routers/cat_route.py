from fastapi import APIRouter, Depends

from db import db
from models.cat_model import CatCreate, NextRoundCatSchema
from auth.token import get_current_user, TokenData


cats_router = APIRouter(prefix="/cats", tags="images")

cats_ref = db.collection("Cats")

@cats_router.post("/create", response_model=NextRoundCatSchema)
async def create_cat(cat: CatCreate, token_data: TokenData = Depends(get_current_user)):
    print(token_data.id)
    return 