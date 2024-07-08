from pydantic import Field, BaseModel


class ImageBase(BaseModel):
    id: str = Field(..., description="Unique identifier for the image")
    file_name: str = Field(..., description="URL where the image is stored")


class ImageBase64(BaseModel):
    photo_base64: str = Field(...)


class Image(ImageBase):
    pass


class ImageUrl(BaseModel):
    image_url: str


class ImageFileName(BaseModel):
    file_name: str


class ImageWithUrl(Image, ImageUrl):
    pass
