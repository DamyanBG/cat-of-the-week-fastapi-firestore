from pydantic import Field, BaseModel


class ImageBase(BaseModel):
    id: str = Field(..., description="Unique identifier for the image")
    image_url: str = Field(..., description="URL where the image is stored")


class ImageCreate(BaseModel):
    photo_base64: str = Field(...)


class ImageResp(ImageBase):
    pass
