from datetime import datetime

from pydantic import BaseModel

from shop_be.schemas.image import ImageSchema


class ProfileSchema(BaseModel):
    id: int
    avatar: ImageSchema
    bio: str
    socials: dict | list | None
    contact: str
    customer_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ShopOwnerSchema(BaseModel):
    id: int
    name: str
    email: str
    email_verified_at: datetime | None
    created_at: datetime
    updated_at: datetime
    is_active: int
    shop_id: int | None = None
    profile: ProfileSchema

    class Config:
        from_attributes = True
