from google.cloud.firestore import FieldFilter

from db import db

image_ref = db.collection("Images")


async def select_image_url_by_id(image_id: str) -> str:
    image_doc = await image_ref.document(image_id).get()
    image_dict = image_doc.to_dict()
    image_url = image_dict["image_url"]
    return image_url
