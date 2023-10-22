from datetime import datetime

from pydantic import BaseModel

from shop_be.schemas.image import ImageSchema


class Settings(BaseModel):
    isHome: bool
    layoutType: str
    productCard: str


class CategoryTypeSchema(BaseModel):
    id: int
    name: str
    language: str
    translated_languages: list[str] = ['en']
    settings: Settings
    slug: str
    icon: str
    promotional_sliders: list[ImageSchema]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BannerSchema(BaseModel):
    id: int
    type_id: int
    title: str
    description: str
    image: ImageSchema
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductTypeSchema(BaseModel):
    id: int
    name: str
    settings: Settings
    slug: str
    language: str
    icon: str
    promotional_sliders: list = []
    created_at: datetime
    updated_at: datetime
    translated_languages: list[str] = ['en']
    banners: list[BannerSchema]

    class Config:
        from_attributes = True
