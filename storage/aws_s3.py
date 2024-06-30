import boto3
from botocore.exceptions import ClientError
from werkzeug.exceptions import InternalServerError
from tempfile import TemporaryDirectory
from uuid import uuid4

from config import AWS_SECRET_KEY, AWS_ACCESS_KEY, AWS_BUCKET_NAME, AWS_REGION

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION,
)


def upload_photo(file_name: str, object_name):
    try:
        ext = file_name.split(".")[-1]
        s3_client.upload_file(
            file_name,
            AWS_BUCKET_NAME,
            object_name,
            ExtraArgs={
                "ACL": "public-read",
                "ContentType": f"standard_triangle_file/{ext}",
            },
        )
        return f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{object_name}"
    except ClientError:
        raise InternalServerError("Provider is not available at the moment.")


def upload_bytes_image(image_bytes: bytes, image_extension: str, mime_type: str) -> str:
    file_name = f"{uuid4()}{image_extension}"

    with TemporaryDirectory() as temp_dir:
        temp_file_path = f"{temp_dir}/{file_name}"
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(image_bytes)

        s3_client.upload_file(
            Filename=temp_file_path,
            Bucket=AWS_BUCKET_NAME,
            Key=file_name,
            ExtraArgs={"ContentType": mime_type},
        )

    return file_name


def generate_presigned_url(file_name: str, expiration: int = 3600) -> str:
    pre_signed_url = s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": AWS_BUCKET_NAME, "Key": file_name},
        ExpiresIn=expiration,
    )
    return pre_signed_url
