from fastapi import APIRouter, HTTPException

from db import db
from utils.image_compression import compress_image_to_webp
from utils.utils import separate_data_url_from_base64
from storage.google_cloud_storage import upload_bytes_image, generate_signed_url
from image_recognition.google_vision import check_is_safe_image
from models.image_model import ImageBase, ImageCreate, ImageResp

images_router = APIRouter(prefix="/images", tags=["images"])

images_ref = db.collection("Images")


@images_router.post("/upload", response_model=ImageResp)
async def create_home(image: ImageCreate):
    """Create a new home listing."""
    data = image.model_dump()
    base64_data = data["photo_base64"]
    image_bytes = compress_image_to_webp(separate_data_url_from_base64(base64_data)[1])
    if not check_is_safe_image(image_bytes):
        raise HTTPException(status_code=400, detail="Image is not safe for work")

    img_file_name = upload_bytes_image(image_bytes, ".webp", "image/webp")
    img_url = generate_signed_url(img_file_name)
    new_image_ref = images_ref.document()

    new_image_data = {"image_url": img_url}
    new_image_ref.set(new_image_data)
    new_image_data["id"] = new_image_ref.id
    return new_image_data
