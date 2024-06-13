from tempfile import TemporaryDirectory
from uuid import uuid4
from datetime import timedelta, datetime, UTC
from google.cloud import storage
from google.cloud.storage.blob import Blob

from sa import credentials
from config import BUCKET_NAME


client = storage.Client(credentials=credentials)


def upload_bytes_image(image_bytes: bytes, image_extension: str, mime_type: str) -> str:
    file_name = f"{uuid4()}{image_extension}"

    with TemporaryDirectory() as temp_dir:
        temp_file_path = f"{temp_dir}/{file_name}"
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(image_bytes)
        bucket = client.get_bucket(BUCKET_NAME)

        # Upload to Google Cloud Storage
        blob = bucket.blob(file_name)
        blob.upload_from_filename(
            temp_file_path, content_type=mime_type
        )  # Set content type

    return file_name


def generate_signed_url(file_name, expiration_hours=1):
    """Generates a signed URL for a blob in Google Cloud Storage.

    Args:
        bucket_name: The name of the GCS bucket.
        file_name: The name of the file within the bucket.
        expiration_hours: The number of hours the URL should be valid for (default 1 hour).

    Returns:
        The signed URL, or None if an error occurred.
    """
    try:
        bucket = client.bucket(BUCKET_NAME)
        blob = Blob(file_name, bucket)

        expiration_time = datetime.now(UTC) + timedelta(hours=expiration_hours)
        signed_url = blob.generate_signed_url(
            version="v4", expiration=expiration_time, method="GET"
        )

        return signed_url
    except Exception as e:
        print(f"Error generating signed URL: {e}")
        return None
