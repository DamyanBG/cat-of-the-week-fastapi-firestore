from fastapi import APIRouter
from routers import cat_route, user_route

api_router = APIRouter()
api_router.include_router(user_route.user_router)
