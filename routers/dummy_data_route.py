from fastapi import APIRouter
from aiofiles import open as asopen
from datetime import date
import json
import asyncio
import base64

from models.user_model import UserCreate
from models.cat_model import CurrentRoundCatCreate, CatCreate, CatOfTheWeekCreate
from models.image_model import ImageFileName
from queries.user_queries import insert_user
from queries.image_queries import insert_image
from queries.cat_queries import (
    insert_current_round_cats,
    create_next_round_cat,
    insert_cat_of_the_week,
)
from storage.google_cloud_storage import upload_bytes_image
from utils.image_compression import compress_image_to_webp
from utils.utils import separate_data_url_from_base64


dummy_data_router = APIRouter(prefix="/load-dummy-data", tags=["dummy", "test", "data"])


@dummy_data_router.post("/")
async def load_dummy_data():
    async with asopen("test_data/users.json", "r") as f:
        user_json = await f.read()
        user_data = json.loads(user_json)
        user_creates = [UserCreate(**user) for user in user_data]

    insert_user_tasks = [insert_user(user) for user in user_creates]
    users = await asyncio.gather(*insert_user_tasks)

    cat_images_file_names = []
    for i in range(1, 4):
        async with asopen(f"test_data/images/cat_image_{i}.webp", "rb") as f:
            image_data = await f.read()
        image_base64 = base64.b64encode(image_data).decode("utf-8")
        base64_with_data_url = f"data:image/webp;base64,{image_base64}"

        image_bytes = compress_image_to_webp(
            separate_data_url_from_base64(base64_with_data_url)[1]
        )
        image_file_name = upload_bytes_image(image_bytes, ".webp", "image/webp")
        cat_images_file_names.append(ImageFileName(file_name=image_file_name))

    insert_image_tasks = [
        insert_image(image_name) for image_name in cat_images_file_names
    ]
    images = await asyncio.gather(*insert_image_tasks)

    async with asopen("test_data/current_round_cats.json", "r") as f:
        crc_json = await f.read()
        crc_data = json.loads(crc_json)
        crc_creates = [
            CurrentRoundCatCreate(photo_id=image.id, user_id=user.id, **cat)
            for cat, image, user in zip(crc_data, images, users)
        ]

    await insert_current_round_cats(crc_creates)

    async with asopen("test_data/next_round_cats.json", "r") as f:
        nrc_json = await f.read()
        nrc_data = json.loads(nrc_json)
        nrc_create = CatCreate(**nrc_data[0], photo_id=images[1].id)

    await create_next_round_cat(nrc_create, users[3].id)

    async with asopen("test_data/images/cat_of_the_week.webp", "rb") as f:
        image_data = await f.read()
        image_base64 = base64.b64encode(image_data).decode("utf-8")
        base64_with_data_url = f"data:image/webp;base64,{image_base64}"

        image_bytes = compress_image_to_webp(
            separate_data_url_from_base64(base64_with_data_url)[1]
        )
        cofw_image_file_name = upload_bytes_image(image_bytes, ".webp", "image/webp")

    cotw_image = await insert_image(ImageFileName(file_name=cofw_image_file_name))

    async with asopen("test_data/cat_of_the_week.json", "r") as f:
        cotw_json = await f.read()
        cotw_data = json.loads(cotw_json)
        current_date = date.today()
        iso_calendar = current_date.isocalendar()
        cotw_create = CatOfTheWeekCreate(
            **cotw_data,
            photo_id=cotw_image.id,
            user_id=users[-1].id,
            year=iso_calendar.year,
            week_number=iso_calendar.week,
        )

    await insert_cat_of_the_week(cotw_create)

    return "OK"
