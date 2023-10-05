from pydantic import BaseModel

from shop_be.schemas.image import ImageSchema


class CategorySchema(BaseModel):
    id: int
    name: str
    slug: str
    language: str
    icon: str | None = None
    image: ImageSchema | None = None
    details: str | None = None
    parent: int
    type_id: int
    created_at: str
    updated_at: str
    deleted_at: str | None = None
    parent_id: int
    translated_languages: list[str]
