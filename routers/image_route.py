from fastapi import APIRouter, HTTPException, status

from queries.image_queries import insert_image
from utils.image_compression import compress_image_to_webp
from utils.utils import separate_data_url_from_base64
from storage.google_cloud_storage import upload_bytes_image, generate_signed_url
from image_recognition.google_vision import check_is_safe_and_contains_cat
from models.image_model import ImageFileName, ImageBase64, ImageWithUrl

images_router = APIRouter(prefix="/images", tags=["images"])


@images_router.post(
    "/upload", response_model=ImageWithUrl, status_code=status.HTTP_201_CREATED
)
async def post_image(image: ImageBase64):
    data = image.model_dump()
    base64_data = data["photo_base64"]
    image_bytes = compress_image_to_webp(separate_data_url_from_base64(base64_data)[1])
    if not check_is_safe_and_contains_cat(image_bytes):
        raise HTTPException(status_code=400, detail="Image is not accepted!")

    img_file_name_str = upload_bytes_image(image_bytes, ".webp", "image/webp")
    img_file_name = ImageFileName(file_name=img_file_name_str)
    new_image = await insert_image(img_file_name)
    img_url = generate_signed_url(new_image.file_name)
    new_image_with_url = ImageWithUrl(
        **{"image_url": img_url}, **new_image.model_dump()
    )

    return new_image_with_url
