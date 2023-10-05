from pydantic import BaseModel

from shop_be.schemas.image import ImageSchema


class BannerSchema(BaseModel):
    id: int
    type_id: int
    title: str
    description: str
    image: ImageSchema
    created_at: str
    updated_at: str


class Settings(BaseModel):
    isHome: bool
    layoutType: str
    productCard: str


class ProductTypeSchema(BaseModel):
    id: int
    name: str
    settings: Settings
    slug: str
    language: str
    icon: str
    promotional_sliders: list = []
    created_at: str
    updated_at: str
    translated_languages: list[str] = ['en']
    banners: list[BannerSchema]
