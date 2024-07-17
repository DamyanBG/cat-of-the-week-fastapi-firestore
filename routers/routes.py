from fastapi import APIRouter
from routers import cat_route, user_route, image_route, vote_route, dummy_data_route

api_router = APIRouter()
api_router.include_router(user_route.user_router)
api_router.include_router(image_route.images_router)
api_router.include_router(cat_route.cats_router)
api_router.include_router(vote_route.vote_router)
api_router.include_router(dummy_data_route.dummy_data_router)
