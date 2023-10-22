from datetime import datetime

from pydantic import BaseModel

from shop_be.schemas.image import ImageSchema


class BaseCategorySchema(BaseModel):
    id: int
    name: str
    slug: str
    icon: str | None = None
    image: list[ImageSchema] = []
    details: str | None = None
    language: str
    translated_languages: list[str]
    type_id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: str | None = None
    parent_id: int
