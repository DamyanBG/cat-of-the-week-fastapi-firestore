from db import db
from models.image_model import Image, ImageFileName

image_ref = db.collection("Images")


async def select_image_file_name_by_id(image_id: str) -> str:
    image_doc = await image_ref.document(image_id).get()
    image_dict = image_doc.to_dict()
    file_name = image_dict["file_name"]
    return file_name


async def insert_image(image_file_name: ImageFileName) -> Image:
    new_image_ref = image_ref.document()
    image_data_dict = image_file_name.model_dump()
    await new_image_ref.set(image_data_dict)
    image_data_dict["id"] = new_image_ref.id
    image = Image(**image_data_dict)
    return image
