from datetime import datetime

from pydantic import BaseModel

from shop_be.schemas.image import ImageSchema


class BaseCategorySchema(BaseModel):
    id: int
    name: str
    slug: str
    icon: str | None = None
    image: ImageSchema | None
    details: str | None = None
    language: str
    translated_languages: list[str]
    created_at: datetime
    updated_at: datetime
    deleted_at: str | None = None
    parent_id: int | None = None

    class Config:
        from_attributes = True
