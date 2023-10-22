from pydantic import BaseModel


class ImageSchema(BaseModel):
    id: int
    original: str
    thumbnail: str

    class Config:
        from_attributes = True
