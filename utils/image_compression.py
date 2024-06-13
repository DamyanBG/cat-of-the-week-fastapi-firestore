from PIL import Image
import io
import base64
import binascii


def compress_image_to_webp(
    base64_image: str, max_size: int = 200 * 1024, quality: int = 85
) -> tuple[bytes, str]:
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
        image_data = base64.b64decode(base64_image)

        if len(image_data) > max_size:
            img = Image.open(io.BytesIO(image_data))

            buffer = io.BytesIO()
            img.save(buffer, format=file_type, lossless=False, quality=quality)
            buffer.seek(0)
            image_data = buffer.read()

        return image_data

    except (binascii.Error, Image.UnidentifiedImageError) as e:  # Catch binascii.Error
        raise ValueError("Invalid image data or format") from e
