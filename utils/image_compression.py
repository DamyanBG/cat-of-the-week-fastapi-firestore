from PIL import Image
from io import BytesIO
from base64 import b64decode
from binascii import Error


def compress_image_to_webp(
    base64_image: str, max_size: int = 200 * 1024, quality: int = 85
) -> bytes:
    """Compresses a Base64-encoded image to WebP format if it exceeds the max size.

    Args:
        base64_image: The Base64-encoded image data.
        max_size: The maximum allowed size in bytes (default: 200KB).
        quality: The desired quality of the WebP image (0-100, default: 85).

    Returns:
        The compressed image data as bytes (WebP if compressed, original if not).
    """
    file_type = "webp"
    try:
        image_data = b64decode(base64_image)

        if len(image_data) > max_size:
            img = Image.open(BytesIO(image_data))

            buffer = BytesIO()
            img.save(buffer, format=file_type, lossless=False, quality=quality)
            buffer.seek(0)
            image_data = buffer.read()

        return image_data

    except (Error, Image.UnidentifiedImageError) as e:
        raise ValueError("Invalid image data or format") from e
