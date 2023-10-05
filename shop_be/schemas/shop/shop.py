from datetime import datetime

from pydantic import BaseModel

from shop_be.schemas.image import ImageSchema


class ShopSchema(BaseModel):
    id: int
    owner_id: int
    name: str
    slug: str
    description: str
    is_active: bool
    cover_image: ImageSchema
    logo: ImageSchema
    address: dict
    settings: dict
    created_at: datetime
    updated_at: datetime
